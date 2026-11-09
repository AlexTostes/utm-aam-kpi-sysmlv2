"""Build the E1 outputs from the SysML v2 model (usage: build_outputs.py <out> <catalog dir>): working spreadsheet (with evidence) and LaTeX tables in the article-1 style."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e1_from_model import catalog   # E1 is a query over the SysML v2 catalog

CAT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "catalog")
def _rows(path):
    return [(r["code"], r["name"], r["principal"], [(i, c, e) for i, c, e, _ in r["inputs"]], r["calc"], r["note"])
            for r in catalog(path)]
UTM, AAM = _rows(os.path.join(CAT, "KPI_UTM.sysml")), _rows(os.path.join(CAT, "KPI_AAM.sysml"))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
ROWS = [("UTM", k) for k in UTM] + [("AAM", k) for k in AAM]
CLASS = {"NS": "Network-shared", "PA": "Provider-archived", "IH": "Internally held", "NA": "Not addressed"}
CALC = {"C1": "Computable from ConOps-defined data", "C2": "Partially computable",
        "C3": "Not computable from ConOps-defined data"}

# ---------------- spreadsheet ----------------
F = "Arial"
hdr, hfill = Font(name=F, bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3A5F")
norm, bold = Font(name=F), Font(name=F, bold=True)
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
fills = {"C1": "E2EFDA", "C2": "FFF2CC", "C3": "F8CBAD"}


def header(ws, row, cols):
    for c, h in enumerate(cols, 1):
        x = ws.cell(row=row, column=c, value=h); x.font = hdr; x.fill = hfill; x.alignment = wrap; x.border = box


wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws["A1"] = "E1 calculability matrix: inputs of the 31 KPI candidates against the FAA UTM ConOps v2.0 and UAM ConOps v2.0"
ws["A1"].font = Font(name=F, bold=True, size=12)
ws["A2"] = "One row per input. Classes and the calculability rule are defined on the Legend sheet. Citations give section and printed page."
ws["A2"].font = Font(name=F, italic=True)
cols = ["Domain", "KPI", "Candidate KPI", "Principal quantity", "Input", "Source class", "Evidence (section, page)",
        "KPI calculability", "Note"]
header(ws, 4, cols)
r = 5
for dom, (code, name, principal, inputs, calc, note) in ROWS:
    for j, (inp, cls, ev) in enumerate(inputs):
        vals = [dom, code, name, principal, inp, cls, ev, calc, note if j == 0 else ""]
        for c, v in enumerate(vals, 1):
            x = ws.cell(row=r, column=c, value=v); x.font = bold if c == 2 else norm; x.alignment = wrap; x.border = box
        ws.cell(row=r, column=8).fill = PatternFill("solid", fgColor=fills[calc])
        r += 1
last_input_row = r - 1
for col, w in zip("ABCDEFGHI", [8, 12, 30, 30, 46, 10, 44, 11, 48]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:I{last_input_row}"

ks = wb.create_sheet("KPI summary")
header(ks, 1, ["Domain", "KPI", "Candidate KPI", "Principal quantity", "Calculability", "Inputs NS", "Inputs PA",
               "Inputs IH", "Inputs NA", "Note"])
for i, (dom, (code, name, principal, inputs, calc, note)) in enumerate(ROWS, start=2):
    vals = [dom, code, name, principal, calc]
    for c, v in enumerate(vals, 1):
        x = ks.cell(row=i, column=c, value=v); x.font = norm; x.alignment = wrap; x.border = box
    ks.cell(row=i, column=5).fill = PatternFill("solid", fgColor=fills[calc])
    for c, cl in zip(range(6, 10), ("NS", "PA", "IH", "NA")):
        x = ks.cell(row=i, column=c, value=f'=COUNTIFS(Inputs!$B$5:$B${last_input_row},$B{i},Inputs!$F$5:$F${last_input_row},"{cl}")')
        x.font = norm; x.border = box
    x = ks.cell(row=i, column=10, value=note); x.font = norm; x.alignment = wrap; x.border = box
for col, w in zip("ABCDEFGHIJ", [8, 12, 34, 34, 12, 9, 9, 9, 9, 60]):
    ks.column_dimensions[col].width = w
ks.freeze_panes = "C2"

cs = wb.create_sheet("Counts")
cs["A1"] = "KPI candidates by calculability class"; cs["A1"].font = bold
header(cs, 2, ["Class", "UTM", "AAM", "Total", "Share of 31"])
n = len(ROWS) + 1
for i, c in enumerate(("C1", "C2", "C3"), start=3):
    cs.cell(row=i, column=1, value=f"{c}: {CALC[c]}").font = norm
    cs.cell(row=i, column=2, value=f"=COUNTIFS('KPI summary'!$A$2:$A${n},\"UTM\",'KPI summary'!$E$2:$E${n},\"{c}\")")
    cs.cell(row=i, column=3, value=f"=COUNTIFS('KPI summary'!$A$2:$A${n},\"AAM\",'KPI summary'!$E$2:$E${n},\"{c}\")")
    cs.cell(row=i, column=4, value=f"=B{i}+C{i}")
    cs.cell(row=i, column=5, value=f"=D{i}/SUM($D$3:$D$5)").number_format = "0.0%"
    for c2 in range(1, 6):
        cs.cell(row=i, column=c2).border = box; cs.cell(row=i, column=c2).font = norm
cs.cell(row=6, column=1, value="Total").font = bold
for c2, L in zip(range(2, 5), "BCD"):
    cs.cell(row=6, column=c2, value=f"=SUM({L}3:{L}5)").font = bold
cs["A8"] = "Inputs by source class"; cs["A8"].font = bold
header(cs, 9, ["Class", "Inputs", "Share"])
for i, c in enumerate(("NS", "PA", "IH", "NA"), start=10):
    cs.cell(row=i, column=1, value=f"{c}: {CLASS[c]}").font = norm
    cs.cell(row=i, column=2, value=f'=COUNTIF(Inputs!$F$5:$F${last_input_row},"{c}")').font = norm
    cs.cell(row=i, column=3, value=f"=B{i}/SUM($B$10:$B$13)").number_format = "0.0%"
cs.column_dimensions["A"].width = 46
for col in "BCDE":
    cs.column_dimensions[col].width = 12

lg = wb.create_sheet("Legend")
lines = [
    ("Source classes", None),
    ("NS - Network-shared", "Exchanged across the USS Network (UTM) or the federated service network (UAM) during operations."),
    ("PA - Provider-archived", "Retained by USSs or PSUs (or by operators) and available on authorized request. A system-level value requires aggregation across providers; neither ConOps defines a performance-measurement aggregator."),
    ("IH - Internally held", "Exists within an operator or a single provider, with no sharing or archiving requirement in the ConOps."),
    ("NA - Not addressed", "No corresponding data element in the ConOps; requires an external source or a new data requirement."),
    ("Calculability rule", None),
    ("C1", "Every input is NS or PA."),
    ("C2", "The principal quantity is NS or PA, but at least one other input is IH or NA."),
    ("C3", "The principal quantity is IH or NA."),
    ("Scope", None),
    ("Inputs", "Minimal quantities implied by each Measurement Construct of article 1 (author-derived; article 1 gives a formula only for UTM-ENV-01)."),
    ("Sources", "FAA, UTM ConOps v2.0 (2020); FAA, UAM ConOps v2.0 (2023). Citations give section and printed page."),
    ("Status", "Analytical classification by the authors; not yet reviewed by independent analysts."),
]
for i, (a, b) in enumerate(lines, start=1):
    lg.cell(row=i, column=1, value=a).font = bold if b is None or len(a) <= 3 or "-" in a else norm
    if b:
        x = lg.cell(row=i, column=2, value=b); x.font = norm; x.alignment = wrap
lg.column_dimensions["A"].width = 26; lg.column_dimensions["B"].width = 100
xlsx = os.path.join(OUT, "E1_calculability_matrix.xlsx")
wb.save(xlsx)

# ---------------- LaTeX (article-1 style: table*, tabularx, booktabs, footnotesize) ----------------
def tex(s):
    s = s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
    s = s.replace("§", r"\S{}").replace(" - ", "--")
    s = re.sub(r"(\d)-(\d)", r"\1--\2", s)
    return s


def short_ev(ev):
    secs = re.findall(r"(§[\d.]+|App\. [A-E])", ev)
    return ", ".join(dict.fromkeys(secs))


def kpi_rows(rows):
    out = []
    for code, name, principal, inputs, calc, note in rows:
        items = []
        for inp, cls, ev in inputs:
            s = short_ev(ev)
            items.append(f"{tex(inp)} [{cls}{'; ' + tex(s) if s else ''}]")
        out.append(f"{code} -- {tex(name)} & {tex(principal)} & {'; '.join(items)} & {calc} \\\\")
    return out


CAPTION = (r"Calculability of the {dom} candidate KPIs from data defined in the FAA {doc}. Source classes: NS, "
           r"network-shared; PA, provider-archived; IH, internally held by an operator or a single provider; NA, not "
           r"addressed. C1: every input is NS or PA; C2: the principal quantity is NS or PA but another input is IH or "
           r"NA; C3: the principal quantity is IH or NA. Inputs are author-derived from the Measurement Constructs; "
           r"section references are to the {short}. The classification is analytical and has not been externally reviewed.")


def table(dom, doc, label, rows):
    t = [r"% E1 calculability matrix (" + dom + r"). Requires: booktabs, tabularx, array (as in article 1).",
         r"\begin{table*}[!t]",
         r"\caption{" + CAPTION.format(dom=dom, doc=doc, short=doc.split(" (")[0]) + "}",
         r"\label{" + label + "}", r"\centering", r"\footnotesize", r"\renewcommand{\arraystretch}{1.12}",
         r"\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.21\textwidth}>{\raggedright\arraybackslash}p{0.17\textwidth}>{\raggedright\arraybackslash}X>{\centering\arraybackslash}p{0.035\textwidth}@{}}",
         r"\toprule",
         r"\textbf{Candidate KPI} & \textbf{Principal quantity} & \textbf{Inputs [source class; ConOps section]} & \textbf{Calc.} \\",
         r"\midrule"]
    t += kpi_rows(rows)
    t += [r"\bottomrule", r"\end{tabularx}", r"\end{table*}", ""]
    return "\n".join(t)


open(os.path.join(OUT, "tab_calculability_utm.tex"), "w").write(table("UTM", "UTM ConOps v2.0", "tab:calc-utm", UTM))
open(os.path.join(OUT, "tab_calculability_aam.tex"), "w").write(
    table("AAM", "UAM ConOps v2.0 (UAM as the urban subset of AAM)", "tab:calc-aam", AAM))

from collections import Counter
cu = Counter(k[4] for k in UTM); ca = Counter(k[4] for k in AAM)
ci = Counter(c for k in UTM + AAM for _, c, _ in k[3])
summary = [r"""% Summary of E1. Requires: booktabs.
\begin{table}[!t]
\caption{Calculability classes of the 31 candidate KPIs (counts of candidates).}
\label{tab:calculability-summary}
\centering
\footnotesize
\renewcommand{\arraystretch}{1.12}
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Class} & \textbf{UTM} & \textbf{AAM} & \textbf{Total} \\
\midrule"""]
for c, lab in (("C1", "C1: computable from ConOps-defined data"), ("C2", "C2: partially computable"),
               ("C3", "C3: not computable from ConOps-defined data")):
    summary.append(f"{lab} & {cu[c]} & {ca[c]} & {cu[c] + ca[c]} \\\\")
summary += [r"\midrule", f"Total & {len(UTM)} & {len(AAM)} & {len(UTM) + len(AAM)} \\\\",
            r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
open(os.path.join(OUT, "tab_calculability_summary.tex"), "w").write("\n".join(summary))
print("UTM", dict(cu), "AAM", dict(ca), "inputs", dict(ci))
