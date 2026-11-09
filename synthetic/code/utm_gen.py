"""Synthetic data generator for UTM.

Produces two tables with the fields of UTM_Selected:
  intents  -> item def OperationalIntent (intentId, isValid, outcome, requestedStart, plannedStart, plannedEnd)
  records  -> item def OperationRecord   (intentId, actualStart, actualEnd)
plus auxiliary columns (uss, cells, hiddenConflict) used by the diagnostics and by E5.

Steps
1. Demand: N ~ Poisson(lambda*T); requested start uniform over the period; submission with a random lead
   time. Each intent crosses k airspace volumes in sequence; each volume is occupied for a fraction of the
   duration (simplified 4D operational intent).
2. Strategic planning (in submission order): the operator's USS searches for the smallest start shift, in
   fixed steps up to the search window, free of conflict with the intents it knows (with a separation
   buffer) and outside active constraints. An accepted intent is shared with the other USSs; each
   transmission fails with probability p (message exchange failure).
3. Execution (in planned-start order): actual start = planned + normal deviation + occasional operator
   lateness; if a volume is still occupied by an operation already under way (undetected conflict or
   propagated delay), the operation waits for it plus a tactical buffer.

Deviations, durations and buffers are illustrative assumptions, not operational data.
"""
import numpy as np
import pandas as pd

Outcomes = ("Accepted", "RejectedConflict", "RejectedConstraint", "RejectedInvalid", "Withdrawn")


def _segments(route, dur):
    k = len(route)
    return [(c, j * dur / k, (j + 1) * dur / k) for j, c in enumerate(route)]


def _conflict(seg_i, a, seg_j, p, buf):
    for ci, o0, o1 in seg_i:
        for cj, q0, q1 in seg_j:
            if ci == cj and a + o0 < p + q1 + buf and p + q0 < a + o1 + buf:
                return True
    return False


def generate(sc, seed):
    rng = np.random.default_rng(seed)
    T = sc.params.periodSeconds
    n = rng.poisson(sc.demandPerHour * T / 3600)

    req = rng.uniform(0, T, n)
    dur = rng.uniform(*sc.durationRange, n)
    sub = req - rng.uniform(*sc.leadTimeRange, n)
    valid = rng.random(n) >= sc.invalidFraction
    uss = rng.integers(0, sc.ussCount, n)
    k = rng.integers(sc.cellsPerRoute[0], sc.cellsPerRoute[1] + 1, n)
    routes = [rng.choice(sc.cells, size=kk, replace=False).tolist() for kk in k]
    segs = [_segments(routes[i], dur[i]) for i in range(n)]

    if sc.constraintActive:                              # dynamic constraint (UVR)
        c_cells = set(rng.choice(sc.cells, size=sc.constraintCells, replace=False).tolist())
        c0 = rng.uniform(0, T - sc.constraintDurationSeconds)
        c1 = c0 + sc.constraintDurationSeconds
    else:
        c_cells, c0, c1 = set(), 0.0, 0.0

    def in_constraint(i, a):
        return any(c in c_cells and a + o0 < c1 and c0 < a + o1 for c, o0, o1 in segs[i])

    # ---------- planning ----------
    order = np.argsort(sub, kind="stable")
    known = [set() for _ in range(sc.ussCount)]
    by_cell = [set() for _ in range(sc.cells)]
    outcome = np.empty(n, dtype=object)
    planned = np.full(n, np.nan)
    hidden = np.zeros(n, dtype=bool)
    shifts = np.arange(0, sc.searchWindowSeconds + 1e-9, sc.shiftStepSeconds)

    for i in order:
        if not valid[i]:
            outcome[i] = "RejectedInvalid"
            continue
        u = uss[i]
        near = set().union(*(by_cell[c] for c in routes[i]))
        cand = [j for j in near if j in known[u]]
        acc = None
        blocked0 = False
        for s in shifts:
            a = req[i] + s
            if in_constraint(i, a):
                blocked0 = blocked0 or s == 0
                continue
            if any(_conflict(segs[i], a, segs[j], planned[j], sc.separationBufferSeconds) for j in cand):
                continue
            acc = a
            break
        if acc is None:
            outcome[i] = "RejectedConstraint" if blocked0 else "RejectedConflict"
            continue
        outcome[i] = "Accepted"
        planned[i] = acc
        hidden[i] = any(_conflict(segs[i], acc, segs[j], planned[j], 0) for j in near - known[u])
        for c in routes[i]:
            by_cell[c].add(i)
        known[u].add(i)
        for v in range(sc.ussCount):
            if v != u and rng.random() >= sc.messageFailureProbability:
                known[v].add(i)

    acc_idx = np.where(outcome == "Accepted")[0]
    outcome[acc_idx[rng.random(len(acc_idx)) < sc.withdrawProbability]] = "Withdrawn"   # accepted, then cancelled

    # ---------- execution ----------
    execd = np.where(outcome == "Accepted")[0]
    execd = execd[np.argsort(planned[execd], kind="stable")]
    act = np.full(n, np.nan)
    busy = [[] for _ in range(sc.cells)]
    for i in execd:
        t = planned[i] + rng.normal(0, sc.startDeviationSigmaSeconds)
        if rng.random() < sc.lateReadinessProbability:
            t += rng.exponential(sc.lateReadinessMeanSeconds)
        for _ in range(50):
            clash = [b1 - o0 for c, o0, o1 in segs[i] for (b0, b1) in busy[c] if t + o0 < b1 and b0 < t + o1]
            if not clash:
                break
            t = max(clash) + sc.tacticalBufferSeconds
        act[i] = t
        for c, o0, o1 in segs[i]:
            busy[c].append((t + o0, t + o1))

    intents = pd.DataFrame({
        "intentId": [f"UTM-{seed}-{i:04d}" for i in range(n)],
        "isValid": valid, "outcome": outcome,
        "requestedStart": req, "plannedStart": planned, "plannedEnd": planned + dur,
        "uss": uss, "cells": [" ".join(map(str, r)) for r in routes],
        "hiddenConflict": hidden, "submitted": sub,
    })
    records = pd.DataFrame({
        "intentId": intents.intentId.values[execd],
        "actualStart": act[execd], "actualEnd": act[execd] + dur[execd],
        "uss": uss[execd],
    })
    return intents, records, {"cells": sc.cells, "hidden_conflicts": int(hidden.sum())}
