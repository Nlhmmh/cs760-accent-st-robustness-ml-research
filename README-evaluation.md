# How to run translation-quality evaluation

[08_evaluation.ipynb](notebooks/08_evaluation.ipynb) is the replication entry
point for WER, BLEU, chrF, chrF++, accent tables, paired descriptive gaps and
literal `<unk>` counts. It evaluates the three archived prediction sets on
CPU; no audio, model weights or new inference are required.

The current archived evaluation files are in
[runs/evaluation_results/](runs/evaluation_results/). The notebook still writes
relative filenames and reads prediction URLs from GitHub `main`. Follow the
local replay setup below to use this checkout and keep regenerated files separate.
These are instructions for configuring a replay copy; the notebook is unchanged.

## Inputs and environment

| System | Prediction file |
|---|---|
| Direct | [direct_predictions.csv](runs/direct_full_run_1788151795/direct_predictions.csv) |
| Cascade-600M | [cascade_predictions.csv](runs/cascade_full_run_1788146589/cascade_predictions.csv) |
| Cascade-3.3B | [cascade_predictions.csv](runs/cascade_full_run_1790228071/cascade_predictions.csv) |

Each file contains 4,200 predictions and metadata. Align clips using unique
`id`, never the repeating speaker identifier `sample_id`. Source sentences,
accent labels and Chinese references must agree across files.

Start from the repository root in a Python environment with:

```bash
python -m pip install pandas==2.3.3 numpy sacrebleu==2.6.0 jiwer matplotlib seaborn tabulate notebook ipykernel
jupyter notebook
```

Select that environment's kernel. Pandas 2.3.3 supports the notebook's
`include_groups=False` calls and matches the inspected local environment.
SacreBLEU 2.6.0 is the version used for the previously verified scores. Other
packages above are not locked to the historical evaluation environment; record
their installed versions for the replay.

## Configure a local replay

Open notebook 08 and make the following changes in your replay copy before
executing the analysis:

1. Omit the opening `import torch`/GPU-information cell. It is informational;
   scoring does not require PyTorch.
2. Replace the first input cell with the setup below. Start the kernel at the
   repository root, or in its `notebooks/` directory.

```python
import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd().resolve()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "runs").is_dir(), "Select the repository working directory"

direct_url = PROJECT_ROOT / "runs/direct_full_run_1788151795/direct_predictions.csv"
cascade_url = PROJECT_ROOT / "runs/cascade_full_run_1788146589/cascade_predictions.csv"
direct = pd.read_csv(direct_url)
cascade = pd.read_csv(cascade_url)

REPLAY_DIR = PROJECT_ROOT / "tmp/evaluation_replay"
REPLAY_DIR.mkdir(parents=True, exist_ok=True)
os.chdir(REPLAY_DIR)  # subsequent relative CSV outputs go here
```

3. In `LOAD CASCADE-3.3B OUTPUT`, replace only `cascade_33b_url` with:

```python
cascade_33b_url = PROJECT_ROOT / "runs/cascade_full_run_1790228071/cascade_predictions.csv"
```

4. Omit the two `!pip install ...` lines after installing dependencies above,
   but execute the imports and calculations in those cells. This keeps the
   selected scoring environment intact.
5. Keep the recorded scoring settings. Do not select settings based on which
   ones increase a system's scores.

The existing remote URLs can be used for an online run, but local files tie
the replay to your checkout. The two Cascade ASR stages were run separately.
The notebook verifies that their archived transcript strings match on all
4,200 clips; that does not mean the same ASR execution was reused.

## Execute the analysis

Restart the kernel, then execute the configured analysis cells in order:

1. Load Direct and Cascade-600M, merge by `id`, and calculate raw and normalized
   WER, including corpus and mean-per-clip summaries.
2. Calculate the initial two-system BLEU and chrF/chrF++ comparisons.
3. Load Cascade-3.3B and run the alignment assertions.
4. Calculate the three-system overall and accent tables, sentence chrF++,
   pairwise gaps and literal `<unk>` summaries.
5. Execute **FINAL CHECK + SAVE ANALYSIS DATAFRAME**.

Stop after the final save cell. The trailing Git clone, Git status and Colab
notebook-export cells are optional housekeeping and are unnecessary for local
evaluation. The three-system section depends on earlier metric objects and
dataframes; do not run it alone in a fresh kernel.

### Scoring settings and interpretation

| Measure | Current calculation |
|---|---|
| Raw WER | Original English reference and Whisper transcript |
| Normalized WER | Lowercase, remove punctuation, collapse spaces and trim |
| BLEU | SacreBLEU with `tokenize="zh"` |
| chrF | Character order 6, word order 0, `beta=2`, default whitespace exclusion |
| chrF++ | Character order 6, word order 2, `beta=2`, default whitespace exclusion |
| Per-clip gaps | First system minus second system's sentence chrF++ |
| Literal `<unk>` | Exact string search in Direct translations |

Corpus translation scores pool metric statistics; they are not averages of
sentence scores. Notebook 09 analyses **mean sentence chrF++**, not corpus BLEU.
The `WER` values in T1 and T4 are mean per-clip WER; the earlier pooled WER
calculation is corpus WER. Direct has no intermediate ASR transcript to score.

Older narrative sections include proposals for later statistics and hypotheses
about `<unk>`. Use notebook 09 and the diagnostic evidence for current conclusions.
Comparing an `<unk>`-free subset with all clips changes the evaluated sample and
does not measure the causal effect of removing the marker.

## Outputs and expected checks

The notebook writes these files into the current working directory, which the
local setup above sets to `tmp/evaluation_replay/`:

| Output | Contents |
|---|---|
| `merged_3system_with_metrics.csv` | Per-clip predictions, sentence chrF++, WER, gaps and `<unk>` flag |
| `table_T1_corpus_metrics.csv` | Overall corpus translation metrics and mean per-clip WER |
| `table_T1b_pairwise_gaps.csv` | Differences between overall corpus translation scores |
| `table_T2_chrfpp_by_accent.csv` | Corpus chrF++ for each accent and system |
| `table_bleu_by_accent_three_systems.csv` | Corpus BLEU and differences by accent |
| `table_macro_micro_chrfpp.csv` | Mean sentence and corpus chrF++ by accent |
| `table_T3_chrfpp_gaps.csv` | Mean sentence chrF++ gaps by accent |
| `table_T4_wer_by_accent.csv` | Mean per-clip normalized WER, standard deviation and counts |
| `table_T5_direct_unk_by_accent.csv` | Counts and rates of literal `<unk>` |
| `table_direct_unk_comparison.csv` | Direct corpus scores for all and `<unk>`-free clips |

The archived evaluation folder currently contains the merged CSV and
[08_evaluation.pdf](runs/evaluation_results/08_evaluation.pdf), rather than all
these individual table CSVs. PDF export is separate from metric computation.

Check 4,200 unique IDs, seven groups of 600, complete references and complete
per-clip metric columns. Expected rounded overall scores are:

| System | Corpus BLEU | Corpus chrF | Corpus chrF++ |
|---|---:|---:|---:|
| Direct | 38.86 | 32.38 | 25.08 |
| Cascade-600M | 29.11 | 24.23 | 18.44 |
| Cascade-3.3B | 31.91 | 26.36 | 20.06 |

Expected literal `<unk>` count is 508. Normalized corpus WER is approximately
5.97%; mean per-clip WER is approximately 6.32%. If results differ, check inputs,
alignment, scoring settings and dependency versions before interpreting changes.
Record SacreBLEU signatures and package versions with the replay.

Pass the regenerated merged CSV directly to notebook 09 using
[README-statistical-analysis.md](README-statistical-analysis.md). There is no
need to replace the archived evaluation CSV to analyse a replay.

## Plotting and current limitations

The notebook displays a normalized-WER histogram using Matplotlib and Seaborn.
It does not currently save that figure or generate the full set of overall,
accent and confidence-interval plots. Retain the notebook output or add a
`savefig` call in the replay if the histogram is required as a separate artifact.
Missing plotting code should be added for any further figures reported in the
final submission.

## Contributions and external resources

The [main contribution table](README.md#team-member-contributions) records
**Patricia Jennesha** for the evaluation notebook and system/accent comparisons,
and **Zhitong Li** for maintaining the shared metric table and statistical input.
The project contribution is prediction alignment, evaluation configuration,
system comparisons and analysis of the selected data.

SacreBLEU implements BLEU and chrF/chrF++; jiwer implements WER and text
transforms. Pandas, NumPy, Matplotlib and Seaborn provide supporting operations.
Metric papers are listed in [references.bib](literature_review/latex/references.bib).
The pretrained model outputs and reference translations retain their external
model/dataset provenance. Any copied or adapted code should be credited with
its original URL and modifications beside the relevant notebook cell.
