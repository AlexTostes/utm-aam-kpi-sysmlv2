# From Candidate KPIs to Computable Indicators: UTM and AAM performance in SysML v2

Model, code and data for the paper *"From Candidate KPIs to Computable Indicators: A SysML v2 Model of UTM
and AAM Performance Anchored in the FAA Concepts of Operations"* (A. S. M. Tostes, D. R. Pleffken and
C. S. Cerqueira; submitted to *IEEE Access*).

The repository contains:
- a SysML v2 library of 31 system-level KPI candidates for Unmanned Aircraft System Traffic Management (UTM)
  and Advanced Air Mobility (AAM), anchored in the FAA UTM ConOps v2.0 and UAM ConOps v2.0;
- the calculability analysis (E1), computed as a query over the model;
- synthetic data generators and experiments (E2–E5) for four prioritized candidates;
- an interactive dashboard of the synthetic results.

> **Scope.** All scenario values are illustrative assumptions. The synthetic results characterize the behaviour
> of the candidates in a model, namely computability, sensitivity and discrimination. They are not empirical
> validation and are not evidence about real UTM or AAM operations.

## Quick start

```bash
pip install -r requirements.txt
./reproduce.sh          # regenerates the library, E1, the conformance check and E2–E5, and compares with the committed outputs
```

The SysML v2 notebooks run in the OMG SysML v2 Pilot Implementation (Jupyter kernel `jupyter-sysml-kernel` 0.62.0,
conda-forge):

```bash
conda create -n sysml -c conda-forge jupyter-sysml-kernel=0.62.0
conda activate sysml
jupyter lab             # open models/catalog/*.ipynb and models/focused/*.ipynb with the "SysML" kernel
```

Run `KPI_Common.ipynb` first; the other notebooks include the shared core.

## Contents

| Path | Content |
|---|---|
| `models/catalog/` | Shared core (`KPI_Common`) and the UTM (14) and AAM (17) candidate libraries, as `.sysml` and `.ipynb` |
| `models/focused/` | `UTM_Selected` and `AAM_Selected`: minimum architecture, data items with source classes, measurement parameters, the four prioritized candidates, analysis case and targets |
| `tools/` | `gen_model.py` (generates the library), `sync_notebooks.py` (copies the `.sysml` sources into the notebooks), `lint.py` (structural check, not a substitute for the Pilot) |
| `e1/` | `e1_from_model.py` (E1 query), `sysml_text.py` (reader of the textual notation), `build_outputs.py` (matrix and LaTeX tables), `schema_check.py` (model–code conformance), `matrix.py` (source classification with evidence, input of `gen_model.py`) |
| `e1/outputs/` | `E1_calculability_matrix.xlsx` and the LaTeX tables of the paper |
| `synthetic/code/` | Parameters, UTM and UAM generators, the four KPIs and their diagnostics, experiments and figures |
| `synthetic/data/` | Logs of one base-case run per domain (seed 20261106), with the fields of the `item def`s |
| `synthetic/results/` | `runs.csv` (one row per run), `summary.csv` (mean and 95% CI per condition), `E3_correlation.csv` |
| `synthetic/figures/` | pgfplots sources, plotted data and PDFs of the figures |
| `dashboard/` | Self-contained HTML dashboard (English and Portuguese) and the data it embeds |

## How the model is used in the analysis

- **Source classes as metadata.** Every input of every candidate carries `@DataSource` (network-shared,
  provider-archived, internally held, not addressed, with the ConOps section and printed page) and
  `@KPIInputRole` (principal or supporting). In the focused models, the class is on the data-item attributes and
  the role on the dependency from the KPI to each attribute.
- **E1 as a query.** `e1/e1_from_model.py` reads the `.sysml` files, collects the annotated inputs and applies the
  rule: C1 if every input is network-shared or provider-archived; C2 if the principal input is, but another is not;
  C3 if the principal input is internally held or not addressed. The reader recovers the containment tree only;
  it is not a SysML v2 parser and assumes models already validated by the Pilot Implementation.
- **Model–code conformance.** `e1/schema_check.py` checks that every data-item attribute a KPI depends on is a
  column of the generated logs, and that every column the KPI code reads is declared in the model.
- **Targets as requirements.** In the focused models, each target specializes its Performance Objective with
  a `require constraint`, is bound to the analysis result, and is asserted of the base case with `satisfy`.
  Target values are illustrative.

## Reproducibility

Seeds are fixed (base seed 20261106; per-condition seeds by CRC32), so `reproduce.sh` regenerates the committed
results byte for byte. Tested with Python 3.13, numpy 2.5, pandas 3.0, scipy 1.18 and openpyxl 3.1. Figures
also need `pdflatex` with `pgfplots`. The FAA concepts of operations are not redistributed here; see the
references in the paper.

## Citation

See `CITATION.cff`. Please cite the paper and, for this material, the archived release (DOI in the badge once
the release is archived on Zenodo).

## License

- Code (`tools/`, `e1/*.py`, `synthetic/code/`, `reproduce.sh`): MIT License, see `LICENSE`.
- Models, data, results, figures and dashboard: Creative Commons Attribution 4.0 International (CC BY 4.0),
  see `LICENSE-CC-BY-4.0.md`.
