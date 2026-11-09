"""KPIs and supporting diagnostic metrics, following the calc defs in UTM_Selected and AAM_Selected."""
import numpy as np


def accommodation_rate(accommodated, valid_demand):          # KPI_Patterns::AccommodationRate
    return 100.0 * accommodated / valid_demand if valid_demand else float("nan")


def temporal_conformance_rate(within, completed):            # KPI_Patterns::TemporalConformanceRate
    return 100.0 * within / completed if completed else float("nan")


# ---------------- UTM ----------------

def utm_cap_01(intents, meas):
    """UTM-CAP-01: valid intents accepted with plannedStart - requestedStart <= Delta / valid intents."""
    v = intents[intents.isValid]
    acc = ((v.outcome == "Accepted") | (v.outcome == "Withdrawn")) & \
          ((v.plannedStart - v.requestedStart) <= meas.shiftWindowSeconds + 1e-9)
    # Withdrawn = accepted, then cancelled by the operator: the demand was accommodated
    return accommodation_rate(int(acc.sum()), len(v))


def utm_pred_01(intents, records, meas):
    """UTM-PRED-01: completed operations with |actualStart - plannedStart| <= tau / completed operations."""
    if records.empty:
        return float("nan")
    m = records.merge(intents[["intentId", "plannedStart"]], on="intentId")
    within = (np.abs(m.actualStart - m.plannedStart) <= meas.toleranceSeconds + 1e-9).sum()
    return temporal_conformance_rate(int(within), len(m))


def utm_diagnostics(intents, records, meas, extra):
    v = intents[intents.isValid]
    rej = v[v.outcome.str.startswith("Rejected")]
    m = records.merge(intents[["intentId", "plannedStart"]], on="intentId")
    dev = np.abs(m.actualStart - m.plannedStart)
    return {
        "rej_conflict_share": float((rej.outcome == "RejectedConflict").mean()) if len(rej) else 0.0,
        "rej_constraint_share": float((rej.outcome == "RejectedConstraint").mean()) if len(rej) else 0.0,
        "intent_density": len(v) / extra["cells"],                  # valid intents per volume in the period
        "start_dev_p95_s": float(np.percentile(dev, 95)) if len(dev) else float("nan"),
        "hidden_conflicts": extra["hidden_conflicts"],
    }


# ---------------- AAM ----------------

def aam_cap_01(requests, meas):
    """AAM-CAP-01: valid requests served with departure shift <= Delta / valid requests."""
    v = requests[requests.isValid]
    acc = (v.outcome == "Confirmed") & ((v.scheduledDeparture - v.requestedDeparture) <= meas.shiftWindowSeconds + 1e-9)
    return accommodation_rate(int(acc.sum()), len(v))


def aam_pred_01(flights, meas):
    """AAM-PRED-01: completed flights with |actualArrival - scheduledArrival| <= tau / completed flights."""
    if flights.empty:
        return float("nan")
    within = (np.abs(flights.actualArrival - flights.scheduledArrival) <= meas.toleranceSeconds + 1e-9).sum()
    return temporal_conformance_rate(int(within), len(flights))


def aam_diagnostics(requests, flights, meas, extra):
    v = requests[requests.isValid]
    den = v[v.outcome.str.startswith("Denied")]
    out = {f"deny_{c}": float((den.outcome == c).mean()) if len(den) else 0.0
           for c in ("DeniedNoPad", "DeniedNoCharge", "DeniedNoAircraft", "DeniedAirspace")}
    T = meas.periodSeconds / 3600
    out["vertiport_throughput_per_h"] = 2 * len(flights) / extra["vertiports"] / T   # movements per vertiport per hour
    out["pad_utilization"] = extra["pad_busy_s"] / (extra["pads_total"] * extra["horizon_s"])
    out["charging_availability"] = 1 - extra["charger_wait_s"] / max(1.0, extra["charger_wait_s"] + extra["charge_s"])
    out["airspace_closed_share"] = extra["closed_share"]
    out["fleet_availability"] = extra["fleet_used"] / extra["fleet"]
    late = flights[(flights.actualArrival - flights.scheduledArrival) > meas.toleranceSeconds]
    for c in ("late_aircraft", "pad_hold", "boarding", "en_route"):
        out[f"delay_{c}"] = float((late.mainCause == c).mean()) if len(late) else 0.0
    return out
