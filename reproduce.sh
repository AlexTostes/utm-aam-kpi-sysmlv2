#!/usr/bin/env bash
# Reproduces the computational results of the paper from this repository and compares them with the
# committed outputs. Takes about a minute. Requires Python 3 with the packages in requirements.txt.
set -euo pipefail
cd "$(dirname "$0")"
OUT=_reproduce
rm -rf "$OUT"; mkdir -p "$OUT"

echo "1/4 Catalog: regenerate the 31-KPI library from the E1 source classification"
python3 tools/gen_model.py "$OUT/catalog" > /dev/null
for f in KPI_Common KPI_UTM KPI_AAM; do cmp -s "$OUT/catalog/$f.sysml" "models/catalog/$f.sysml" && echo "   $f.sysml identical"; done

echo "2/4 E1: calculability as a query over the SysML v2 models"
python3 e1/e1_from_model.py models/catalog models/focused
python3 e1/build_outputs.py "$OUT/e1" models/catalog > /dev/null
for f in tab_calculability_utm.tex tab_calculability_aam.tex tab_calculability_summary.tex; do
  cmp -s "$OUT/e1/$f" "e1/outputs/$f" && echo "   $f identical"; done

echo "3/4 Conformance between the focused models and the KPI code"
python3 e1/schema_check.py models/focused synthetic/code/kpis.py synthetic/data

echo "4/4 Synthetic experiments E2-E5 (30 replications per condition)"
mkdir -p "$OUT/synthetic"
(cd synthetic/code && python3 run_experiments.py "../../$OUT/synthetic" 30 > /dev/null)
for f in results/summary.csv results/E3_correlation.csv data/UTM_OperationIntent_base.csv data/AAM_FlightRecord_base.csv; do
  cmp -s "$OUT/synthetic/$f" "synthetic/$f" && echo "   $f identical" || echo "   $f DIFFERS"; done
echo "Done. Figures: cd synthetic/code && python3 make_figures.py .. (needs pdflatex with pgfplots)."
