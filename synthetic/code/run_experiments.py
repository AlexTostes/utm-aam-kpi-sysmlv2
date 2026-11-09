"""Experiments E2-E5 of the article-2 proposal on synthetic data.

Usage: python run_experiments.py <output_dir> [replications]
Writes results/*.csv and data/ (logs of one base-case run per domain). Figures: make_figures.py.
"""
import os, sys, zlib
import numpy as np
import pandas as pd
from scipy import stats

from params import UTMScenario, AAMScenario, MeasurementParameters, with_, MIN
import utm_gen, aam_gen, kpis

OUT = os.path.abspath(sys.argv[1])
R = int(sys.argv[2]) if len(sys.argv) > 2 else 30
for d in ("results", "figures", "data"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


SEED0 = 20261106


def h(tag):                                         # deterministic seed offset per condition
    return zlib.crc32(tag.encode()) % 9973


def run_utm(sc, tag, **lab):
    rows = []
    for r in range(R):
        I, Rr, X = utm_gen.generate(sc, SEED0 + 1000 * (h(tag)) + r)
        row = dict(domain="UTM", experiment=tag, rep=r, **lab,
                   CAP=kpis.utm_cap_01(I, sc.params), PRED=kpis.utm_pred_01(I, Rr, sc.params),
                   n_valid=int(I.isValid.sum()), n_completed=len(Rr))
        row.update(kpis.utm_diagnostics(I, Rr, sc.params, X))
        rows.append(row)
    return rows


def run_aam(sc, tag, **lab):
    rows = []
    for r in range(R):
        Q, F, X = aam_gen.generate(sc, SEED0 + 1000 * (h(tag)) + r)
        row = dict(domain="AAM", experiment=tag, rep=r, **lab,
                   CAP=kpis.aam_cap_01(Q, sc.params), PRED=kpis.aam_pred_01(F, sc.params),
                   n_valid=int(Q.isValid.sum()), n_completed=len(F))
        row.update(kpis.aam_diagnostics(Q, F, sc.params, X))
        rows.append(row)
    return rows


U0, A0 = UTMScenario(), AAMScenario()
allrows = []

# E2a: sensitivity to demand
for lam in (20, 60, 90, 120, 150, 180, 240, 300):
    allrows += run_utm(with_(U0, demandPerHour=lam), f"E2a-{lam}", factor="demand", level=lam)
for lam in (10, 20, 30, 40, 50, 60, 80, 100):
    allrows += run_aam(with_(A0, peakDemandPerHour=lam), f"E2a-{lam}", factor="demand", level=lam)

# E2b: sensitivity to tau and Delta in the base case (same logs, only the measurement changes)
def remeasure_utm(levels, field):
    rows = []
    for r in range(R):
        I, Rr, X = utm_gen.generate(U0, SEED0 + 77 + r)
        for v in levels:
            m = MeasurementParameters(U0.params.periodSeconds,
                                      v if field == "tau" else U0.params.toleranceSeconds,
                                      v if field == "delta" else U0.params.shiftWindowSeconds)
            rows.append(dict(domain="UTM", experiment=f"E2b-{field}", rep=r, factor=field, level=v,
                             CAP=kpis.utm_cap_01(I, m), PRED=kpis.utm_pred_01(I, Rr, m)))
    return rows


def remeasure_aam(levels, field):
    rows = []
    for r in range(R):
        Q, F, X = aam_gen.generate(A0, SEED0 + 77 + r)
        for v in levels:
            m = MeasurementParameters(A0.params.periodSeconds,
                                      v if field == "tau" else A0.params.toleranceSeconds,
                                      v if field == "delta" else A0.params.shiftWindowSeconds)
            rows.append(dict(domain="AAM", experiment=f"E2b-{field}", rep=r, factor=field, level=v,
                             CAP=kpis.aam_cap_01(Q, m), PRED=kpis.aam_pred_01(F, m)))
    return rows


allrows += remeasure_utm([30, 60, 120, 300], "tau") + remeasure_utm([0, 300, 600, 900], "delta")
allrows += remeasure_aam([2 * MIN, 5 * MIN, 10 * MIN, 15 * MIN], "tau") + remeasure_aam([0, 300, 600, 900], "delta")

# E4: trade-off through the buffer (operational lever), at two demand levels
for lam in (120, 200):
    for b in (0, 30, 60, 120, 240):
        allrows += run_utm(with_(U0, demandPerHour=lam, separationBufferSeconds=b), f"E4-{lam}-{b}",
                           factor="buffer", level=b, demand=lam)
for lam in (40, 60):
    for b in (0, 2 * MIN, 5 * MIN, 10 * MIN):
        allrows += run_aam(with_(A0, peakDemandPerHour=lam, scheduleBufferSeconds=b), f"E4-{lam}-{b}",
                           factor="buffer", level=b, demand=lam)

# E5: federated aggregation in UTM (number of USSs x message exchange failure)
fed = []
for nu in (1, 3, 5):
    for p in (0.0, 0.05, 0.10, 0.20, 0.40):
        if nu == 1 and p > 0:
            continue
        sc = with_(U0, ussCount=nu, messageFailureProbability=p)
        tag = f"E5-{nu}-{p}"
        for r in range(R):
            I, Rr, X = utm_gen.generate(sc, SEED0 + 1000 * (h(tag)) + r)
            row = dict(domain="UTM", experiment="E5", rep=r, factor="federation", uss=nu, pfail=p,
                       CAP=kpis.utm_cap_01(I, sc.params), PRED=kpis.utm_pred_01(I, Rr, sc.params),
                       hidden_conflicts=X["hidden_conflicts"])
            per = []
            for u in range(nu):
                Iu, Ru = I[I.uss == u], Rr[Rr.uss == u]
                per.append(kpis.utm_pred_01(Iu, Ru, sc.params))
            row["PRED_uss_min"], row["PRED_uss_max"] = np.nanmin(per), np.nanmax(per)
            fed.append(row)
allrows += fed

df = pd.DataFrame(allrows)
df.to_csv(os.path.join(OUT, "results", "runs.csv"), index=False)


def ci(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan
    return x.mean(), h


summ = []
df["demand"] = df["demand"].fillna(-1)
for (dom, fac, lev, dem), g in df[df.experiment != "E5"].groupby(["domain", "factor", "level", "demand"]):
    for k in ("CAP", "PRED"):
        m, hw = ci(g[k]); summ.append(dict(domain=dom, factor=fac, level=lev, demand=dem, kpi=k, mean=m, ci95=hw, n=len(g)))
for (nu, p), g in df[df.experiment == "E5"].groupby(["uss", "pfail"]):
    for k in ("CAP", "PRED", "hidden_conflicts", "PRED_uss_min", "PRED_uss_max"):
        m, hw = ci(g[k]); summ.append(dict(domain="UTM", factor="federation", level=f"{int(nu)} USS, p={p}", demand=-1, kpi=k, mean=m, ci95=hw, n=len(g)))
S = pd.DataFrame(summ)
S.to_csv(os.path.join(OUT, "results", "summary.csv"), index=False)

# E3: discrimination (CAP x PRED correlation)
corr = []
for dom in ("UTM", "AAM"):
    base_lev = 120 if dom == "UTM" else 40
    sets = {
        "base-case replications (random variation only)": df[(df.domain == dom) & (df.factor == "demand") & (df.level == base_lev)],
        "demand sweep (all runs)": df[(df.domain == dom) & (df.factor == "demand")],
    }
    for dem in sorted(df[(df.domain == dom) & (df.factor == "buffer")].demand.unique()):
        sets[f"buffer sweep, demand {int(dem)}/h"] = df[(df.domain == dom) & (df.factor == "buffer") & (df.demand == dem)]
    for name, g in sets.items():
        g = g.dropna(subset=["CAP", "PRED"])
        r, pr = stats.pearsonr(g.CAP, g.PRED); rho, ps = stats.spearmanr(g.CAP, g.PRED)
        corr.append(dict(domain=dom, run_set=name, n=len(g), pearson_r=r, pearson_p=pr, spearman_rho=rho, spearman_p=ps))
C = pd.DataFrame(corr)
C.to_csv(os.path.join(OUT, "results", "E3_correlation.csv"), index=False)

# example logs (the synthetic data itself)
I, Rr, _ = utm_gen.generate(U0, SEED0)
I.to_csv(os.path.join(OUT, "data", "UTM_OperationIntent_base.csv"), index=False)
Rr.to_csv(os.path.join(OUT, "data", "UTM_OperationRecord_base.csv"), index=False)
Q, F, _ = aam_gen.generate(A0, SEED0)
Q.to_csv(os.path.join(OUT, "data", "AAM_TripRequest_base.csv"), index=False)
F.to_csv(os.path.join(OUT, "data", "AAM_FlightRecord_base.csv"), index=False)

print(S[S.factor.isin(["demand", "buffer"])].pivot_table(index=["domain", "factor", "demand", "level"], columns="kpi", values="mean").round(1).to_string())
print(C.round(3).to_string())
print(S[S.factor == "federation"].pivot_table(index="level", columns="kpi", values="mean").round(2).to_string())
