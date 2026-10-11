# How to run the Q1–Q9 synthesis

[10_synthesis_q1_q9.ipynb](notebooks/10_synthesis_q1_q9.ipynb), authored by
**Jidni Mayukh**, brings the project's nine research questions together using
the existing evaluation, statistical and diagnostic evidence. It also adds
CPU calculations, saves six figures, and builds a self-contained HTML dashboard.

The archived outputs are in [runs/synthesis_results/](runs/synthesis_results/).
To view them without running code, open
[dashboard.html](runs/synthesis_results/dashboard.html) in a browser. Its images
are embedded, so the downloaded page works offline. The
[results README](runs/synthesis_results/README.md) describes the dashboard panels.

## Inputs and environment

No audio, model weights or new inference are required. Use the repository's
existing outputs together, with their original scoring and statistical settings:

| Input | Used for |
|---|---|
| [Merged evaluation CSV](runs/evaluation_results/merged_3system_with_metrics.csv) | Predictions, references, normalized WER, sentence chrF++, system gaps, speaker IDs and `<unk>` flags |
| [Statistical results](runs/statistical_analysis_results/) | `intervals_long.csv`, `accent_means_ci.csv`, `spearman.csv`, `tests.csv` |
| [Accent diagnostic results](unk_analysis/results/accent/) | `<unk>` rates and logistic tests |
| [Word-type results](unk_analysis/results/word_type/) | Word-frequency and proper-noun summaries |
| [Text-only results](unk_analysis/results/text_only/) | `run_summary_unk_extra_1_text.json` |
| [Word-removal results](unk_analysis/results/word_removal/) | `occlusion_sentences.csv` and `unk_trigger_summary.csv` |
| [Decoding sensitivity results](runs/direct_unk_sensitivity_1789954497/) | `translation_metrics_by_condition.csv` and `unk_rate_by_condition.csv` |
| [Literal-marker blocking results](runs/direct_literal_unk_blocking_1789970452/) | `translation_metric_comparison.csv` |

If regenerating upstream evidence, follow [README-evaluation.md](README-evaluation.md)
and [README-statistical-analysis.md](README-statistical-analysis.md) first.
Notebook 10's relative input paths select the archived files; update those paths
together if you want to synthesise a new replay rather than the archive.

For local Jupyter, start from the repository root and install:

```bash
python -m pip install pandas==2.3.3 numpy==2.0.2 scipy==1.13.1 matplotlib==3.9.4 sacrebleu==2.6.0 tabulate==0.9.0 notebook ipykernel
jupyter notebook
```

These versions provide the inspected project's local analysis environment;
they are not a complete record of the environment that produced Jidni's saved
execution. SacreBLEU 2.6.0 is explicitly pinned in notebook 10. The notebook's
installation cell installs only SacreBLEU and tabulate, so the other imports
must already be available in the selected kernel. Keep pandas 2.x for the
current `groupby.apply` sampling behaviour.

## Configure a replay

The setup cell searches the current directory and its parent for
`runs/statistical_analysis_results/intervals_long.csv`. From a complete local
checkout, start the kernel at the repository root or inside `notebooks/`.
The notebook then changes its working directory to the detected repository root.

If no checkout is found, the setup clones GitHub `main`, normally under
`/content/` on Colab. This needs Git and network access. For a fixed replay,
use an existing checkout at the intended commit and record its commit SHA.
An existing clone is not automatically updated by this setup cell.

The setup accepts the merged CSV at its current location under
`runs/evaluation_results/`, with the older `runs/` location as a fallback.
Confirm the printed root and selected input before proceeding.

By default, the notebook writes into `runs/synthesis_results/`, replacing files
with the same names. To preserve the archive, change this line in a replay copy:

```python
OUT = ROOT / "tmp" / "synthesis_replay"
```

Make that change before `FIG = OUT / "figures"` and its directory-creation line.
Keep `SEED = 760` and `N_BOOT = 1000` to compare with the saved analysis. No
notebook extraction to a Python script is needed.

## Execute the notebook

1. Select the prepared CPU kernel and restart it.
2. Run the configured notebook cells in order. The setup, input loading,
   metric helpers and Q1–Q9 sections depend on earlier cells.
3. Confirm the loading checks: 4,200 unique clips, seven groups of 600,
   1,586 speakers, complete predictions/references and 508 Direct `<unk>` clips.
4. Allow the metric recalculations and bootstrap checks to finish. Under Q5,
   an assertion compares the reduced resampler's full-set overall intervals
   with notebook 09's archived intervals before calculating subset intervals.
5. Run the dashboard and README generation cells after all six figures exist.
6. The final ZIP cell is optional. It writes `synthesis_results.zip` at the
   repository root, including the current `OUT` folder's contents. For a replay,
   change the ZIP destination to `ROOT / "synthesis_replay"` if needed.

On Colab, download the generated ZIP from the file panel. Locally, open the
generated dashboard directly. The notebook does not push results to GitHub.
Keep the executed replay notebook and record inputs, package versions, metric
signatures, commit SHA, seed and resample count.

## Outputs

The current archive contains seven CSVs, six PNGs, the dashboard and its README:

| Output | Contents |
|---|---|
| [intervals_unk_free.csv](runs/synthesis_results/intervals_unk_free.csv) | 24 speaker-bootstrap gap rows: three comparisons, overall and seven accents, on the common 3,692-clip `<unk>`-free subset |
| [table_q5_scores_by_unk_subset.csv](runs/synthesis_results/table_q5_scores_by_unk_subset.csv) | All three systems scored on all, `<unk>`-free and affected clips; nine rows |
| [table_q6_scores_by_asr_error.csv](runs/synthesis_results/table_q6_scores_by_asr_error.csv) | Mean sentence scores and gaps for zero-WER and positive-WER clips; two rows |
| [worst_clips_by_accent_system.csv](runs/synthesis_results/worst_clips_by_accent_system.csv) | Ten lowest sentence-chrF++ clips per accent and system; 210 rows |
| [table_q8_worst_clip_summary.csv](runs/synthesis_results/table_q8_worst_clip_summary.csv) | Summaries of those worst-clip sets; 21 rows |
| [table_q9_fallback_check.csv](runs/synthesis_results/table_q9_fallback_check.csv) | Direct versus substituting Cascade-3.3B on the 508 affected clips; two rows |
| [table_q9_one_clip_per_speaker.csv](runs/synthesis_results/table_q9_one_clip_per_speaker.csv) | Three gap intervals after selecting one existing clip per speaker |
| [dashboard.html](runs/synthesis_results/dashboard.html) | Offline HTML summary with embedded figures |
| [README.md](runs/synthesis_results/README.md) | Generated dashboard and result descriptions |

The figures are:

| Figure | Shows |
|---|---|
| [q1_overall_scores.png](runs/synthesis_results/figures/q1_overall_scores.png) | Overall corpus metrics and mean sentence chrF++ |
| [q2_per_accent_gaps.png](runs/synthesis_results/figures/q2_per_accent_gaps.png) | Paired mean sentence chrF++ gaps with intervals by accent |
| [q3_accent_means.png](runs/synthesis_results/figures/q3_accent_means.png) | Accent means with speaker-bootstrap intervals |
| [q5_unk_subsets.png](runs/synthesis_results/figures/q5_unk_subsets.png) | Corpus chrF++ for all, `<unk>`-free and affected clips |
| [q6_wer_and_spearman.png](runs/synthesis_results/figures/q6_wer_and_spearman.png) | Accent-level WER summaries and WER association intervals |
| [q7_scale_lift.png](runs/synthesis_results/figures/q7_scale_lift.png) | Cascade-3.3B minus Cascade-600M gaps by accent |

## Expected results and interpretation

The recomputed overall BLEU scores should round to **38.86**, **29.11** and
**31.91** for Direct, Cascade-600M and Cascade-3.3B. The archived overall mean
sentence chrF++ gaps are **7.00**, **4.99** and **2.01**, respectively for Direct
minus 600M, Direct minus 3.3B and 3.3B minus 600M.

Additional saved checks include:

- 2,952 zero-WER clips and 1,248 positive-WER clips.
- A fallback corpus chrF++ of 24.89, compared with Direct's 25.08 on the same
  full set. This evaluates one specific substitution rule.
- A one-clip-per-speaker Direct-minus-3.3B mean gap of 4.69, with interval
  3.94–5.51, using 1,586 existing clips.

Compare rows by their labels, statistics and sampling units. Notebook 10's
`intervals_unk_free.csv` has its own schema and includes all three comparisons;
it should not be assumed identical to notebook 09's generated subset file.

Read the written conclusions alongside the research-design limitations:

- Corpus scores and mean sentence scores are different quantities.
- Removing `<unk>` clips changes the sample; the score change is not a causal
  estimate of how much the marker alone lowers quality.
- Zero-WER and positive-WER clips are observational groups. Their score
  differences do not isolate the causal effect of ASR errors.
- The one-clip-per-speaker check is a sensitivity analysis of the existing
  dataset, not a held-out evaluation on new data. Its sample is not balanced
  at 600 clips per accent, and its bootstrap is not accent-stratified.
- Proposed improvements and their expected costs are recommendations, not
  completed experiments. The worst-clip audit is not bilingual human review.

## Contributions and sources

**Jidni's contribution:** the Q1–Q9 synthesis notebook, additional subset and
sensitivity calculations, worst-clip audit, six figures, dashboard and generated
results README. The notebook also records his earlier base two-system evaluation.

The synthesis builds on Arizona's dataset and extended diagnostics, Nathan's
inference and earlier sensitivity runs, Patricia's three-system evaluation, and
Zhitong's statistical tables. Its reduced `StratifiedBoot` explicitly reuses
Zhitong's notebook 09 implementation; that reuse should retain its attribution.

External implementations include SacreBLEU, NumPy, pandas, SciPy and Matplotlib.
Model and dataset sources are described in the [main README](README.md#project-work-and-external-resources),
and methodological references are in [references.bib](literature_review/latex/references.bib).
Credit any copied or adapted online code with its original URL beside the cell.
This guide was checked against source and saved outputs; it does not represent
a fresh execution of notebook 10.
