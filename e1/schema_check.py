"""Conformance between the SysML v2 focused models and the synthetic-data code.

(1) every data-item attribute a KPI depends on in the model is a column of the generated log;
(2) every log column the KPI code reads is an attribute the KPI depends on in the model.
Usage: schema_check.py <focused dir> <kpis.py> <data dir>
"""
import csv, inspect, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sysml_text import parse

foc, kpis_py, data = sys.argv[1:4]
LOGS = {"OperationIntent": "UTM_OperationIntent_base.csv", "OperationRecord": "UTM_OperationRecord_base.csv",
        "TripRequest": "AAM_TripRequest_base.csv", "FlightRecord": "AAM_FlightRecord_base.csv"}
FUNCS = {"UTM-CAP-01": "utm_cap_01", "UTM-PRED-01": "utm_pred_01", "AAM-CAP-01": "aam_cap_01", "AAM-PRED-01": "aam_pred_01"}
cols = {k: next(csv.reader(open(os.path.join(data, v)))) for k, v in LOGS.items()}
src = open(kpis_py).read()
fsrc = {code: re.search(rf"def {f}\(.*?(?=\ndef |\Z)", src, re.S).group(0) for code, f in FUNCS.items()}
ok = True
for fn in ("UTM_Selected.sysml", "AAM_Selected.sysml"):
    pkg = parse(open(os.path.join(foc, fn), encoding="utf-8").read()).children[0]
    kpis = {m.group(2): m.group(1) for d in pkg.children if (m := re.match(r"calc def <'([^']+)'>\s+(\w+)", d.header))}
    deps = {}
    for d in pkg.children:
        m = re.match(r"dependency \w+ from (\w+) to (\w+)::(\w+)$", d.header)
        if m and m.group(1) in kpis:
            deps.setdefault(kpis[m.group(1)], set()).add((m.group(2), m.group(3)))
    for code, used in deps.items():
        logged = {(i, a) for i, a in used if i in cols}
        missing_in_log = {f"{i}::{a}" for i, a in logged if a not in cols[i]}
        read = set(re.findall(r"\.(\w+)", fsrc[code])) | set(re.findall(r'"(\w+)"', fsrc[code]))
        log_items = {i for i, _ in logged}
        read_attrs = {(i, w) for i in log_items for w in read if w in cols[i] and w != "intentId" and w != "requestId"}
        # attributes read by the code from the KPI's own items but not declared as KPI inputs in the model
        undeclared = {f"{i}::{a}" for i, a in read_attrs if (i, a) not in used}
        print(f"{code}: model inputs {len(used)} ({len(logged)} logged); missing in log {sorted(missing_in_log) or 'none'}; "
              f"read by code but not in model {sorted(undeclared) or 'none'}")
        ok &= not missing_in_log and not undeclared
print("conformant" if ok else "NOT conformant")
sys.exit(0 if ok else 1)
