"""Synthetic data generator for UAM (the urban subset of AAM).

Produces two tables with the fields of AAM_Selected:
  requests -> item def TripRequest  (requestId, isValid, outcome, requestedDeparture)
  flights  -> item def FlightRecord (requestId, scheduledDeparture, scheduledArrival, actualDeparture, actualArrival)
plus auxiliary columns (origin, destination, aircraft, scheduledDeparture on requests, mainCause).

Steps
1. Fixed network: V vertiports with pads and chargers, flight times between pairs, one corridor per pair.
   Each corridor may close once in the period (window known at planning time).
2. Demand: N ~ Poisson(lambda*T) requests with requested departure uniform over the period and a random O-D pair.
3. Nominal planning (in requested-departure order): searches for the smallest departure shift, in fixed steps
   up to the search window, with the corridor open, an aircraft ready at the origin (recharged, plus a
   schedule buffer), a free pad for boarding at the origin and for deboarding at the destination. Each
   aircraft's schedule only grows forward; recharging after each flight is allocated to a destination charger.
4. Stochastic execution (in scheduled-departure order): boarding, flight time and charging vary; delays
   propagate along the aircraft rotation; on arrival, if no pad is free, the aircraft holds.

Times, capacities and variabilities are illustrative assumptions, not operational data.
"""
import numpy as np
import pandas as pd


def network(sc):
    r = np.random.default_rng(sc.networkSeed)
    V = sc.vertiportCount
    ft = np.zeros((V, V))
    for a in range(V):
        for b in range(a + 1, V):
            ft[a, b] = ft[b, a] = r.uniform(*sc.flightTimeRange)
    return ft


def _count_overlap(intervals, t0, t1):
    return sum(1 for a, b in intervals if a < t1 and t0 < b)


def _charger_slot(chargers, t0, length):
    """Earliest start >= t0 at which some charger is free for 'length'. Returns (start, charger)."""
    best = None
    for k, ivs in enumerate(chargers):
        cands = [t0] + [b for a, b in ivs if b > t0]
        for s in sorted(cands):
            if all(not (a < s + length and s < b) for a, b in ivs):
                if best is None or s < best[0]:
                    best = (s, k)
                break
    return best


def generate(sc, seed):
    rng = np.random.default_rng(seed)
    T = sc.params.periodSeconds
    V = sc.vertiportCount
    ft = network(sc)
    mean_ft = ft[ft > 0].mean()
    half = sc.turnaroundSeconds / 2                     # half for deboarding, half for boarding

    closures = {}
    for a in range(V):
        for b in range(a + 1, V):
            if rng.random() < sc.corridorClosureProbability:
                c0 = rng.uniform(0, T - sc.corridorClosureSeconds)
                closures[(a, b)] = (c0, c0 + sc.corridorClosureSeconds)

    def closed(o, d, t0, t1):
        w = closures.get((min(o, d), max(o, d)))
        return w is not None and t0 < w[1] and w[0] < t1

    n = rng.poisson(sc.peakDemandPerHour * T / 3600)
    req = np.sort(rng.uniform(0, T, n))
    orig = rng.integers(0, V, n)
    dest = (orig + rng.integers(1, V, n)) % V
    valid = rng.random(n) >= sc.invalidFraction

    # ---------- planning ----------
    ac_loc = np.arange(sc.fleetSize) % V
    ac_ready = np.zeros(sc.fleetSize)
    pads = [[] for _ in range(V)]
    chargers = [[[] for _ in range(sc.chargersPerVertiport)] for _ in range(V)]
    outcome = np.empty(n, dtype=object)
    sdep = np.full(n, np.nan)
    sarr = np.full(n, np.nan)
    acft = np.full(n, -1)
    charge_len = {}
    shifts = np.arange(0, sc.searchWindowSeconds + 1e-9, sc.shiftStepSeconds)
    reason_name = {"air": "DeniedAirspace", "aircraft": "DeniedNoAircraft",
                   "charge": "DeniedNoCharge", "pad": "DeniedNoPad"}

    for i in range(n):
        if not valid[i]:
            outcome[i] = "DeniedInvalid"
            continue
        o, d = orig[i], dest[i]
        first_reason = None
        for s in shifts:
            dep = req[i] + s
            arr = dep + ft[o, d]
            reason = None
            here = np.where(ac_loc == o)[0]
            ready = here[ac_ready[here] + sc.scheduleBufferSeconds <= dep - half]
            if closed(o, d, dep, arr):
                reason = "air"
            elif len(ready) == 0:
                reason = "charge" if len(here) else "aircraft"
            elif _count_overlap(pads[o], dep - half, dep) >= sc.padsPerVertiport or \
                    _count_overlap(pads[d], arr, arr + half) >= sc.padsPerVertiport:
                reason = "pad"
            if reason:
                first_reason = first_reason or reason
                continue
            a = ready[np.argmin(ac_ready[ready])]
            ch = sc.chargingSeconds * ft[o, d] / mean_ft
            cs, k = _charger_slot(chargers[d], arr + half, ch)
            chargers[d][k].append((cs, cs + ch))
            pads[o].append((dep - half, dep))
            pads[d].append((arr, arr + half))
            ac_loc[a], ac_ready[a] = d, cs + ch
            outcome[i], sdep[i], sarr[i], acft[i] = "Confirmed", dep, arr, a
            charge_len[i] = ch
            break
        else:
            outcome[i] = reason_name[first_reason]

    # ---------- execution ----------
    served = np.where(outcome == "Confirmed")[0]
    served = served[np.argsort(sdep[served], kind="stable")]
    act_ready = np.zeros(sc.fleetSize)
    apads = [[] for _ in range(V)]
    achg = [[[] for _ in range(sc.chargersPerVertiport)] for _ in range(V)]
    adep = np.full(n, np.nan)
    aarr = np.full(n, np.nan)
    cause = np.empty(n, dtype=object)
    charger_wait = charge_total = 0.0
    for i in served:
        a, o, d = acft[i], orig[i], dest[i]
        board0 = max(sdep[i] - half, act_ready[a])
        late_ac = max(0.0, act_ready[a] - (sdep[i] - half))
        board = max(30.0, half + rng.normal(0, sc.turnaroundSigmaSeconds / np.sqrt(2)))
        extra = rng.exponential(sc.boardingDelayMeanSeconds) if rng.random() < sc.boardingDelayProbability else 0.0
        dep = max(sdep[i], board0 + board + extra)
        apads[o].append((board0, dep))
        fly = ft[o, d] * (1 + rng.normal(0, sc.flightTimeCV))
        t = dep + fly
        hold = 0.0
        for _ in range(50):
            busy = [b for x, b in apads[d] if x < t + half and t < b]
            if len(busy) < sc.padsPerVertiport:
                break
            nt = min(busy) + 1.0
            hold += nt - t
            t = nt
        arr = t
        deb = max(30.0, half + rng.normal(0, sc.turnaroundSigmaSeconds / np.sqrt(2)))
        apads[d].append((arr, arr + deb))
        ch = max(60.0, charge_len[i] + rng.normal(0, sc.chargingSigmaSeconds))
        cs, k = _charger_slot(achg[d], arr + deb, ch)
        achg[d][k].append((cs, cs + ch))
        charger_wait += cs - (arr + deb)
        charge_total += ch
        act_ready[a] = cs + ch
        adep[i], aarr[i] = dep, arr
        comps = {"late_aircraft": late_ac, "boarding": extra + max(0.0, board - half),
                 "en_route": fly - ft[o, d], "pad_hold": hold}
        cause[i] = max(comps, key=comps.get)

    requests = pd.DataFrame({
        "requestId": [f"AAM-{seed}-{i:04d}" for i in range(n)],
        "isValid": valid, "outcome": outcome,
        "requestedDeparture": req, "scheduledDeparture": sdep,
        "origin": orig, "destination": dest,
    })
    flights = pd.DataFrame({
        "requestId": requests.requestId.values[served],
        "scheduledDeparture": sdep[served], "scheduledArrival": sarr[served],
        "actualDeparture": adep[served], "actualArrival": aarr[served],
        "aircraft": acft[served], "origin": orig[served], "destination": dest[served],
        "mainCause": cause[served],
    })
    horizon = max(T, float(np.nanmax(aarr)) if len(served) else T)
    extra = {
        "vertiports": V, "pads_total": V * sc.padsPerVertiport, "horizon_s": horizon,
        "pad_busy_s": sum(b - a for p in apads for a, b in p),
        "charger_wait_s": charger_wait, "charge_s": charge_total,
        "closed_share": sum(w[1] - w[0] for w in closures.values()) / (V * (V - 1) / 2 * T),
        "fleet_used": int(len(np.unique(acft[served]))), "fleet": sc.fleetSize,
    }
    return requests, flights, extra
