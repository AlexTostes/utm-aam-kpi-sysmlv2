"""Figures for experiments E2-E5 as TikZ/pgfplots sources, in the graphic style of article 1.

Style (article 1): black strokes at 0.6 pt, \\footnotesize text, no colour or fills, \\columnwidth figures.
Series are told apart by marker and dash pattern, never by colour. Error bars are 95% CIs.

For each figure this script writes
  figures/<name>.tex     the tikzpicture, to \\input inside a figure environment (inherits the paper's font)
  figures/<name>.pdf     a standalone build of the same picture (Times), for preview or \\includegraphics
and figures/data/*.dat with the plotted values (pgfplots tables).

Usage: python make_figures.py <results_dir>
Requires pdflatex with pgfplots for the PDF builds.
"""
import os, subprocess, sys, shutil
import pandas as pd

OUT = os.path.abspath(sys.argv[1])
S = pd.read_csv(os.path.join(OUT, "results", "summary.csv"))
FIG = os.path.join(OUT, "figures")
DAT = os.path.join(FIG, "data")
os.makedirs(DAT, exist_ok=True)

KPI = {("UTM", "CAP"): "UTM-CAP-01", ("UTM", "PRED"): "UTM-PRED-01",
       ("AAM", "CAP"): "AAM-CAP-01", ("AAM", "PRED"): "AAM-PRED-01"}

PREAMBLE = r"""% Requires: \usepackage{pgfplots} \pgfplotsset{compat=1.17} \usepgfplotslibrary{groupplots}
% Style follows the article-1 figures: black, 0.6 pt strokes, \footnotesize, no colour.
"""
STYLE = r"""\pgfplotsset{
  a2/.style={width=\linewidth, height=4.2cm, font=\footnotesize, line width=0.6pt,
    axis line style={line width=0.6pt}, tick style={line width=0.6pt, black},
    every axis label/.append style={font=\footnotesize}, tick label style={font=\footnotesize},
    legend style={draw=none, fill=none, font=\footnotesize, cells={anchor=west}},
    ymajorgrids, grid style={line width=0.3pt, draw=black!15}, axis x line*=bottom, axis y line*=left,
    error bars/error bar style={line width=0.5pt}, error bars/error mark options={rotate=90, mark size=1.5pt}},
  capS/.style={black, solid, mark=*, mark size=1.5pt},
  predS/.style={black, densely dashed, mark=square, mark size=1.6pt, mark options={solid}},
  lowS/.style={black, solid, mark=*, mark size=1.5pt},
  highS/.style={black, densely dashed, mark=triangle, mark size=2pt, mark options={solid}},
}
"""


def write_dat(name, df, cols):
    p = os.path.join(DAT, name + ".dat")
    df[cols].to_csv(p, sep=" ", index=False, float_format="%.3f")
    return f"figures/data/{name}.dat"


def series(dom, fac, kpi, demand=-1):
    g = S[(S.domain == dom) & (S.factor == fac) & (S.kpi == kpi) & (S.demand == demand)].copy()
    g["level"] = g.level.astype(float)
    return g.sort_values("level")


figs = {}

# ---------- Fig. E2a: sensitivity to demand (two stacked panels) ----------
parts = []
for i, (dom, base, unit) in enumerate((("UTM", 120, "operational intents/h"), ("AAM", 40, "trip requests/h"))):
    paths = {}
    for k in ("CAP", "PRED"):
        g = series(dom, "demand", k).rename(columns={"level": "x", "mean": "y", "ci95": "e"})
        paths[k] = write_dat(f"E2a_{dom}_{k}", g, ["x", "y", "e"])
    leg = (r"\legend{capacity KPI (UTM-CAP-01 / AAM-CAP-01), predictability KPI (UTM-PRED-01 / AAM-PRED-01)}"
           if i == 1 else "")
    parts.append(rf"""\nextgroupplot[ylabel={{KPI value (\%)}}, xlabel={{Demand ({unit})}}, ymin=0, ymax=105,
  title={{({'ab'[i]}) {dom}}}, title style={{at={{(0,1)}}, anchor=south west, font=\footnotesize}},
  legend style={{at={{(0.5,-0.42)}}, anchor=north}}]
\addplot[capS, error bars/.cd, y dir=both, y explicit] table[x=x, y=y, y error=e] {{{paths['CAP']}}};
\addplot[predS, error bars/.cd, y dir=both, y explicit] table[x=x, y=y, y error=e] {{{paths['PRED']}}};
{leg}
\draw[densely dotted, line width=0.6pt] (axis cs:{base},0) -- (axis cs:{base},105) node[pos=0.97, right, font=\scriptsize] {{base case}};""")
figs["fig_E2a_demand"] = (r"""\begin{tikzpicture}
\begin{groupplot}[a2, group style={group size=1 by 2, vertical sep=1.5cm}]
""" + "\n".join(parts) + r"""
\end{groupplot}
\end{tikzpicture}
""")

# ---------- Fig. E2b: sensitivity to the measurement specification (2 x 2) ----------
parts = []
letters = iter("abcd")
for dom in ("UTM", "AAM"):
    for fac, k, xl, style in (("tau", "PRED", r"Tolerance $\tau$ (min)", "predS"),
                              ("delta", "CAP", r"Shift window $\Delta$ (min)", "capS")):
        g = series(dom, fac, k)
        g = g.assign(x=g.level / 60, y=g["mean"], e=g.ci95, lab=g["mean"].round(0).astype(int))
        p = write_dat(f"E2b_{dom}_{fac}", g, ["x", "y", "e", "lab"])
        base = {("UTM", "tau"): 1, ("AAM", "tau"): 5, ("UTM", "delta"): 5, ("AAM", "delta"): 10}[(dom, fac)]
        yl = r", ylabel={KPI value (\%)}" if (dom, fac) == ("UTM", "tau") else ""
        parts.append(rf"""\nextgroupplot[xlabel={{{xl}}}, ymin=0, ymax=118, ytick={{0,25,50,75,100}}{yl},
  title={{({next(letters)}) {dom}, {KPI[(dom, k)]}}}, title style={{at={{(0,1)}}, anchor=south west, font=\footnotesize}},
  nodes near coords, point meta=explicit symbolic, every node near coord/.append style={{font=\scriptsize, anchor=south, yshift=1pt}}]
\addplot[{style}, error bars/.cd, y dir=both, y explicit] table[x=x, y=y, y error=e, meta=lab] {{{p}}};
\draw[densely dotted, line width=0.6pt] (axis cs:{base},0) -- (axis cs:{base},118);""")
figs["fig_E2b_tau_delta"] = (r"""\begin{tikzpicture}
\begin{groupplot}[a2, height=4.0cm, group style={group size=4 by 1, horizontal sep=0.9cm},
  width=0.27\linewidth]
""" + "\n".join(parts) + r"""
\end{groupplot}
\end{tikzpicture}
""")

# ---------- Fig. E4: capacity-predictability trade-off (two stacked panels) ----------
parts = []
for i, (dom, dems, unit, lever, fmt) in enumerate((
        ("UTM", (120, 200), "intents/h", "separation buffer", lambda b: f"{b:.0f}\\,s"),
        ("AAM", (40, 60), "requests/h", "schedule buffer", lambda b: f"{b / 60:.0f}\\,min"))):
    plots = []
    for dem, style in zip(dems, ("lowS", "highS")):
        cap = series(dom, "buffer", "CAP", dem); pred = series(dom, "buffer", "PRED", dem)
        g = pd.DataFrame({"x": cap["mean"].values, "ex": cap.ci95.values, "y": pred["mean"].values,
                          "ey": pred.ci95.values,
                          "lab": [fmt(b) if j in (0, len(cap) - 1) else "{}" for j, b in enumerate(cap.level)]})
        p = write_dat(f"E4_{dom}_{dem}", g, ["x", "ex", "y", "ey", "lab"])
        plots.append(rf"""\addplot[{style}, nodes near coords, point meta=explicit symbolic,
  every node near coord/.append style={{font=\scriptsize, anchor=south west, xshift=1pt, yshift=1pt}},
  error bars/.cd, x dir=both, x explicit, y dir=both, y explicit]
  table[x=x, y=y, x error=ex, y error=ey, meta=lab] {{{p}}};""")
    parts.append(rf"""\nextgroupplot[xlabel={{{KPI[(dom, 'CAP')]} (\%)}}, ylabel={{{KPI[(dom, 'PRED')]} (\%)}},
  title={{({'ab'[i]}) {dom}, {lever}}}, title style={{at={{(0,1)}}, anchor=south west, font=\footnotesize}},
  legend style={{at={{(0.5,-0.42)}}, anchor=north}}, enlarge x limits=0.12, enlarge y limits=0.12]
""" + "\n".join(plots) + "\n" + (r"\legend{base demand (UTM 120 intents/h; AAM 40 requests/h), high demand (UTM 200 intents/h; AAM 60 requests/h)}" if i == 1 else ""))
figs["fig_E4_tradeoff"] = (r"""\begin{tikzpicture}
\begin{groupplot}[a2, height=4.6cm, group style={group size=1 by 2, vertical sep=1.6cm}]
""" + "\n".join(parts) + r"""
\end{groupplot}
\end{tikzpicture}
""")

# ---------- Fig. E5: federated aggregation in UTM (three stacked panels) ----------
F = S[S.factor == "federation"].copy()
F["uss"] = F.level.str.extract(r"(\d+) USS")[0].astype(int)
F["p"] = F.level.str.extract(r"p=([\d.]+)")[0].astype(float) * 100
parts = []
for i, (k, yl) in enumerate((("CAP", r"UTM-CAP-01 (\%)"), ("PRED", r"UTM-PRED-01 (\%)"),
                             ("hidden_conflicts", "Undetected conflicts per run"))):
    plots = []
    for nu, style in ((3, "lowS"), (5, "highS")):
        g = F[(F.uss == nu) & (F.kpi == k)].sort_values("p").rename(columns={"p": "x", "mean": "y", "ci95": "e"})
        pth = write_dat(f"E5_{k}_{nu}", g, ["x", "y", "e"])
        plots.append(rf"\addplot[{style}, error bars/.cd, y dir=both, y explicit] table[x=x, y=y, y error=e] {{{pth}}};")
    ref = F[(F.uss == 1) & (F.kpi == k)]
    extra = ""
    if len(ref) and k != "hidden_conflicts":
        v = ref["mean"].iloc[0]
        extra = (rf"\draw[densely dotted, line width=0.6pt] (axis cs:-2,{v:.2f}) -- (axis cs:42,{v:.2f}) "
                 rf"node[right, font=\scriptsize] {{single USS}};")
    leg = r"\legend{3 USSs, 5 USSs}" if i == 0 else ""
    parts.append(rf"""\nextgroupplot[ylabel={{{yl}}}, xlabel={{Message exchange failure probability (\%)}}, xmin=-2, xmax=52,
  title={{({'abc'[i]})}}, title style={{at={{(0,1)}}, anchor=south west, font=\footnotesize}}, legend pos=north west]
""" + "\n".join(plots) + "\n" + leg + "\n" + extra)
figs["fig_E5_federation"] = (r"""\begin{tikzpicture}
\begin{groupplot}[a2, height=3.8cm, group style={group size=1 by 3, vertical sep=1.5cm}]
""" + "\n".join(parts) + r"""
\end{groupplot}
\end{tikzpicture}
""")

# ---------- write sources and build standalone PDFs ----------
with open(os.path.join(FIG, "pgfstyle.tex"), "w") as f:
    f.write("% \\input once in the preamble, after \\usepackage{pgfplots}\n" + STYLE)
for name, body in figs.items():
    with open(os.path.join(FIG, name + ".tex"), "w") as f:
        f.write(PREAMBLE + body)

WIDTH = {"fig_E2b_tau_delta": "7.16in"}   # double-column figure
build = os.path.join(FIG, "_build")
os.makedirs(build, exist_ok=True)
ok = shutil.which("pdflatex") is not None
for name in figs:
    if not ok:
        break
    doc = (r"""\documentclass[border=2pt]{standalone}
\usepackage{times}\usepackage{amsmath}
\usepackage{pgfplots}\pgfplotsset{compat=1.17}\usepgfplotslibrary{groupplots}
\input{figures/pgfstyle.tex}
\begin{document}
\begin{minipage}{%s}\setlength{\linewidth}{%s}
\input{figures/%s.tex}
\end{minipage}
\end{document}
""" % (WIDTH.get(name, "3.5in"), WIDTH.get(name, "3.5in"), name))
    src = os.path.join(build, name + ".tex")
    open(src, "w").write(doc)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={build}", src],
                       cwd=OUT, capture_output=True, text=True)
    if r.returncode:
        print(name, "FAILED"); print(r.stdout[-2500:]); sys.exit(1)
    shutil.copy(os.path.join(build, name + ".pdf"), os.path.join(FIG, name + ".pdf"))
shutil.rmtree(build, ignore_errors=True)
print(sorted(f for f in os.listdir(FIG)))
