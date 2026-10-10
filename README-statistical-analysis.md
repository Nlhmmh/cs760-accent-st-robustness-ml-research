# How to run statistical analysis

[09_statistical_analysis.ipynb](notebooks/09_statistical_analysis.ipynb) is the
replication entry point for confidence intervals, accent comparisons, rank
tests and WER associations. Run it after notebook 08, or use the archived
[merged evaluation CSV](runs/evaluation_results/merged_3system_with_metrics.csv).
This is a CPU analysis; audio, model weights and new inference are unnecessary.

The current notebook contains saved execution output and reads the evaluation
CSV from `runs/evaluation_results/`. Its first installation cell still says
`scip`, and its opening text mentions `statistical_analysis.py`. There is no
standalone script with that name: execute the notebook. The final `sys.argv`
value is an argument-parser label, not a file that must exist.

## Inputs and environment

Required columns are:

```text
id, sample_id, primary_accent, wer_norm,
chrfpp_direct, chrfpp_600m, chrfpp_33b, direct_has_unk
```

`id` must be unique. `sample_id` is the repeating speaker identifier. The
three sentence chrF++ columns must be numeric and complete for the frozen set.
Existing gap columns are checked if present; the notebook recomputes gaps from
the three scores. Missing WER is excluded from correlation analysis, while
missing sentence chrF++ is dropped before the main analysis and reported.

Start Jupyter from the repository root:

```bash
python -m pip install pandas==2.3.3 numpy==2.0.2 scipy==1.13.1 notebook ipykernel
jupyter notebook
```

These pandas, NumPy and SciPy versions match the inspected local environment;
this is not a complete lockfile for every historical run. Select that kernel.
Omit the first `%pip install numpy pandas scip` cell after setup, or correct
`scip` to `scipy` in your replay copy. `scip` is a different package and is not
the SciPy dependency imported by the analysis.

## Configure the notebook

In the project-path cell, confirm the root, select the evaluation CSV, and
choose a separate output directory. For a replay, replace that cell with:

```python
from pathlib import Path

PROJECT_ROOT = Path.cwd().resolve()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "runs").is_dir(), "Select the repository working directory"

# Use the archived evaluation, or change this to tmp/evaluation_replay/... .
DATA_FILE = PROJECT_ROOT / "runs/evaluation_results/merged_3system_with_metrics.csv"
OUTPUT_DIR = PROJECT_ROOT / "tmp/statistical_analysis_replay"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
assert DATA_FILE.is_file(), DATA_FILE
```

The notebook's default root finder looks for both `data/` and `runs/`. If a
fresh clone has no `data/` and the kernel starts inside `notebooks/`, it may
select the wrong root; the explicit setup above handles that case. Start a
fresh kernel before configuring this path. If replaying notebook 08 and 09 in
the same kernel, restore the repository working directory first because the
evaluation guide changes it to the replay output folder.

Keep `SEED = 760` and `N_BOOT = 1000` for comparison with archived results.
Increasing the bootstrap count changes the generated intervals and should be
recorded as a new analysis configuration.

## Execute the notebook

1. Restart the kernel and execute the imports and configured path cell.
2. Execute the constants, input preparation, bootstrap, correlation and test
   function cells in order.
3. Execute the cell defining `main()`.
4. Execute the final cell:

```python
sys.argv = ["statistical_analysis.py"]
main()
```

This calls the functions already defined in the notebook. It uses `DATA_FILE`,
`OUTPUT_DIR`, `N_BOOT` and `SEED` as defaults. Do not call `main()` alone before
resetting `sys.argv`, because Jupyter may supply unrelated command-line flags.
To override the settings in the final cell instead, use:

```python
sys.argv = [
    "statistical_analysis.py",
    "--data", str(DATA_FILE),
    "--out", str(OUTPUT_DIR),
    "--B", "1000",
    "--seed", "760",
]
main()
```

## What the analysis calculates

| Analysis | Calculation and interpretation |
|---|---|
| System gaps | Mean sentence chrF++ for first system minus second system |
| Paired uncertainty | 1,000 accent-stratified resamples; the same sampled rows are used for all systems; 95% percentile intervals |
| Main resampling unit | Speakers, retaining their clips together within each accent |
| Sensitivity resampling | Individual clips; does not preserve speaker dependence |
| Accent means and spread | Mean sentence chrF++; spread is highest minus lowest accent mean |
| WER associations | Clip-level Spearman correlations, with speaker/clip bootstrap intervals overall and by accent |
| Accent differences | Kruskal–Wallis tests at clip and speaker-mean levels |
| Pairwise accent comparisons | Dunn tests for system gaps, with Holm correction within each set of accent pairs |
| Paired system rank tests | Wilcoxon signed-rank tests and paired rank-biserial effects |
| Accent-pair effect sizes | Cliff's delta |
| Accent ordering | Spearman agreement between the seven accent means across systems |
| `<unk>` sensitivity | Remove the same 508 Direct-affected clips from every system, then recalculate Direct-gap intervals |

Speaker-bootstrap estimates remain weighted by clip counts; they are not equal
averages of speaker means. Speaker-level rank tests, in contrast, operate on
speaker means. A `unit="speaker"` correlation row describes the resampling
unit, not a correlation calculated from speaker-averaged observations.

These intervals describe mean sentence chrF++ and its gaps, not corpus BLEU or
corpus chrF++. Repeated sentence content is not jointly modelled with speakers.
Holm correction applies to the Dunn accent pairs in each family; the notebook
does not correct every reported test together. An interval covering zero does
not prove two systems are equivalent, and correlation does not prove causation.

## Outputs and expected checks

The replay writes five CSVs to `OUTPUT_DIR`:

| Output | Contents | Current archived rows |
|---|---|---:|
| [intervals_long.csv](runs/statistical_analysis_results/intervals_long.csv) | Paired gaps, system spreads and spread differences; speaker/clip results | 54 |
| [accent_means_ci.csv](runs/statistical_analysis_results/accent_means_ci.csv) | Accent means, overall means, spreads, intervals and accent ranks | 54 |
| [spearman.csv](runs/statistical_analysis_results/spearman.csv) | WER associations with scores and gaps | 64 |
| [tests.csv](runs/statistical_analysis_results/tests.csv) | Rank tests, adjusted Dunn comparisons and effect sizes | 189 |
| `intervals_unk_free.csv` | Direct-gap sensitivity on the common `<unk>`-free subset | Not currently archived |

The existing [results folder](runs/statistical_analysis_results/) also contains
[09_statistical_analysis.pdf](runs/statistical_analysis_results/09_statistical_analysis.pdf)
and method/Q3/Q4 write-ups. PDF export is separate from computation. The final
saved notebook output reports `<unk>`-free computation, but that fifth CSV is
absent from the current folder; retain it when making a new replay.

Confirm 4,200 input clips, seven accents and 1,586 speakers. For the archived
input and configuration, the rounded overall speaker-bootstrap results are:

| Comparison | Mean sentence chrF++ gap | 95% interval |
|---|---:|---:|
| Direct minus Cascade-600M | 7.00 | 6.45 to 7.60 |
| Direct minus Cascade-3.3B | 4.99 | 4.39 to 5.70 |
| Cascade-3.3B minus Cascade-600M | 2.01 | 1.61 to 2.42 |

Compare regenerated rows by their labels and resampling unit, not just CSV row
position. Compare numeric results with a stated tolerance, retaining full
precision for calculations and rounding only for display. Investigate different
inputs, versions, seed or bootstrap count before treating changes as findings.
Record those settings with the replay.

## Plotting and contributions

The current notebook writes tables and prints summaries; it does not generate
or save statistical figures. Add plotting cells here for any confidence-interval
or association figures included in the final report, using these output tables
and clearly naming the statistic and resampling unit.

The [main contribution table](README.md#team-member-contributions) records
**Zhitong Li** for this statistical implementation and the shared metric table.
The project contribution includes paired speaker/clip resampling, accent
comparisons, association analysis and result-table generation. NumPy, pandas
and SciPy provide external library implementations. Bootstrap and metric
background references are in [references.bib](literature_review/latex/references.bib).
Any copied or adapted implementation should have its original URL and changes
credited beside the relevant notebook cell; method citations alone do not
identify borrowed code.
