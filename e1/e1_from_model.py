"""Experiment E1 as a query over the SysML v2 model.

Catalog (KPI_UTM.sysml, KPI_AAM.sysml): every KPI calc def owns KPIInput attributes annotated with
@DataSource (source class, ConOps reference) and @KPIInputRole (principal or supporting).
Focused models (UTM_Selected, AAM_Selected): the KPI reaches data-item attributes through dependencies
annotated with @KPIInputRole; the attributes carry @DataSource.
The calculability rule is applied to what the query returns:
  C1 every input is NetworkShared or ProviderArchived
  C2 the principal input is NetworkShared or ProviderArchived, another input is InternallyHeld or NotAddressed
  C3 the principal input is InternallyHeld or NotAddressed
Usage: e1_from_model.py <catalog dir> <focused dir> [json out]
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sysml_text import parse, text_of, metadata

ABBR = {"NetworkShared": "NS", "ProviderArchived": "PA", "InternallyHeld": "IH", "NotAddressed": "NA"}
DEFINED = {"NS", "PA"}


def rule(inputs):
    """inputs: list of (role, class)."""
    principal = [c for r, c in inputs if r == "Principal"]
    assert len(principal) == 1, inputs
    if principal[0] not in DEFINED:
        return "C3"
    return "C1" if all(c in DEFINED for _, c in inputs) else "C2"


def catalog(path):
    root = parse(open(path, encoding="utf-8").read())
    rows = []
    for node in root.walk():
        m = re.match(r"calc def <'([A-Z]+-[A-Z]+-\d+)'>\s+(\w+)", node.header)
        if not m:
            continue
        code, name = m.groups()
        title = re.match(r"\S+ -- ([^.]+)\.", text_of(node)).group(1)
        inputs = []
        for a in node.find(r"^attribute input\d+ : KPIInput$"):
            ds, rl = metadata(a, "DataSource"), metadata(a, "KPIInputRole")
            inputs.append((text_of(a), ABBR[ds["sourceClass"]], ds["conopsRef"], rl["role"]))
        rows.append({"code": code, "element": name, "name": title,
                     "principal": text_of(node, "comment", "principalQuantity"),
                     "inputs": inputs, "calc": rule([(r, c) for _, c, _, r in inputs]),
                     "note": text_of(node, "comment", "calculabilityNote") or ""})
    return rows


def focused(path):
    root = parse(open(path, encoding="utf-8").read())
    pkg = root.children[0]
    attr_src = {}
    for d in pkg.children:
        m = re.match(r"(?:item|part) def (\w+)", d.header)
        if m:
            for a in d.children:
                ma = re.match(r"attribute (\w+)\s*:", a.header)
                ds = metadata(a, "DataSource") if ma else None
                if ds:
                    attr_src[f"{m.group(1)}::{ma.group(1)}"] = (ABBR[ds["sourceClass"]], ds["conopsRef"])
    kpis = {}
    for d in pkg.children:
        m = re.match(r"calc def <'([^']+)'>\s+(\w+)", d.header)
        if m:
            kpis[m.group(2)] = m.group(1)
    found = {}
    for d in pkg.children:
        m = re.match(r"dependency (\w+) from (\w+) to (\w+::\w+)$", d.header)
        if m and m.group(2) in kpis and m.group(3) in attr_src:
            role = metadata(d, "KPIInputRole")["role"]
            cls, ref = attr_src[m.group(3)]
            found.setdefault(kpis[m.group(2)], []).append((m.group(3), cls, ref, role))
    return {k: {"inputs": v, "calc": rule([(r, c) for _, c, _, r in v])} for k, v in found.items()}


if __name__ == "__main__":
    cat_dir, foc_dir = sys.argv[1], sys.argv[2]
    utm, aam = catalog(os.path.join(cat_dir, "KPI_UTM.sysml")), catalog(os.path.join(cat_dir, "KPI_AAM.sysml"))
    foc = {**focused(os.path.join(foc_dir, "UTM_Selected.sysml")), **focused(os.path.join(foc_dir, "AAM_Selected.sysml"))}
    from collections import Counter
    print("catalog", len(utm), len(aam), "inputs", sum(len(r["inputs"]) for r in utm + aam))
    print("UTM", Counter(r["calc"] for r in utm), "AAM", Counter(r["calc"] for r in aam))
    print("inputs by class", Counter(c for r in utm + aam for _, c, _, _ in r["inputs"]))
    cat = {r["code"]: r["calc"] for r in utm + aam}
    for k, v in foc.items():
        print("focused", k, v["calc"], "catalog", cat[k], "OK" if v["calc"] == cat[k] else "MISMATCH",
              [(a, c, r[0]) for a, c, _, r in v["inputs"]])
    if len(sys.argv) > 3:
        json.dump({"UTM": utm, "AAM": aam, "focused": foc}, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
