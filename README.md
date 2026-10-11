# Regional English Accent Robustness in Speech Translation

COMPSCI 760 research project comparing how regional English accents are
associated with the translation quality of Direct and Cascaded
speech-to-text translation systems.

The repository contains Group 9's data-preparation and frozen-model inference
notebooks, three completed full runs, three-system quality evaluation,
statistical-analysis tables, a Q1–Q9 synthesis with figures and a dashboard,
an integrated IEEE LaTeX literature survey, and
Direct `<unk>` diagnostics and sensitivity experiments.
**Last updated: 11 October 2026.**

Project code: [GitHub repository](https://github.com/Nlhmmh/cs760-accent-st-robustness-ml-research).

Start with [evaluation results](#evaluation-results),
[reproducing the results](#reproducing-the-results), and
[team-member contributions](#team-member-contributions). Notebook running guides:
[preprocessing](README-preprocessing.md), [model inference](README-running-pipelines.md),
[evaluation](README-evaluation.md), [statistical analysis](README-statistical-analysis.md),
and [Q1–Q9 synthesis](READEME-synthesis.md).

Both Cascaded model variants have completed full runs on all **4,200 clips**,
using Whisper large-v2 for ASR:

| Cascaded MT model | Completed run directory |
|---|---|
| NLLB-200 distilled **600M** | [`cascade_full_run_1788146589`](runs/cascade_full_run_1788146589/) |
| NLLB-200 **3.3B** | [`cascade_full_run_1790228071`](runs/cascade_full_run_1790228071/) |

The implemented experiment has advanced
beyond the proposal: the original design specified five accent groups and
3,000 clips, whereas the frozen dataset and completed runs use **seven accent
groups and 4,200 clips**.

## Research question

> How does regional English accent affect the translation quality of Direct
> and Cascaded speech-to-text translation systems?

The study benchmarks existing pretrained systems; it does not train a new
speech-translation model. Its conclusions should describe observed system and
accent associations, not claim that accent or architecture is the sole causal
explanation for a performance difference.

The original motivation, five-group plan, feasibility analysis, risks, and
team roles are recorded in [`9_Proposal.pdf`](presentation/9_Proposal.pdf).
This README documents the current implemented state when it differs from that
proposal.

## Research design

Both systems process the same frozen English clips and are scored against the
same Simplified Chinese reference translations.

```text
                                    +-------------------------------+
English speech -------------------->| SeamlessM4T v2-large          |
        |                           | Direct speech translation     |
        |                           +---------------+---------------+
        |                                           |
        |                                           v
        |                                  Direct Chinese text
        |
        |                           +-------------------------------+
        +-------------------------->| Whisper large-v2             |
                                    | English ASR                   |
                                    +---------------+---------------+
                                                    |
                                                    v
                                           English transcript
                                                    |
                                    +---------------+---------------+
                                    | NLLB-200 3.3B                 |
                                    | English-to-Chinese MT         |
                                    +---------------+---------------+
                                                    |
                                                    v
                                           Cascaded Chinese text

Direct text and Cascaded text ------> same CoVoST 2 Chinese reference
                                      chrF / chrF++ / BLEU
Whisper transcript -----------------> Common Voice English transcript
                                      normalized WER diagnostic
```

### Direct system

- Architecture: English speech directly to Chinese text.
- Model: `facebook/seamless-m4t-v2-large`.
- Model class: `SeamlessM4Tv2ForSpeechToText`.
- Target-language code: `cmn`.
- Frozen revision used by the completed run:
  `5f8cc790b19fc3f67a61c105133b20b34e3dcb76`.
- No exposed intermediate transcript, fine-tuning, or accent adaptation.

### Cascaded system

- Architecture: English speech to English ASR text to Chinese MT text.
- ASR: `openai/whisper-large-v2`, forced to English transcription.
- Current MT: `facebook/nllb-200-3.3B` (completed 24 September 2026).
- Earlier baseline: `facebook/nllb-200-distilled-600M`; its full run is retained.
- NLLB language direction: `eng_Latn` to `zho_Hans`.
- Frozen revisions resolved by the completed run:
  - Whisper: `ae4642769ce2ad8fc292556ccea8e901f1530655`.
  - NLLB 3.3B: `1a07f7d195896b2114afcb79b7b57ab512e7b43e`.
  - Earlier NLLB 600M: `f8d333a098d19b4fd9a8b18f94170487ad3f821d`.
- Whisper processes every clip first; it is then released before NLLB runs on
  the saved ASR transcripts. NLLB never receives the Common Voice reference
  transcript.

### Shared inference controls

- One fixed configuration for every clip and accent group.
- Deterministic greedy generation: `num_beams=1`, `do_sample=False`, and
  `max_new_tokens=256`.
- Seed: `760`.
- Checkpoint interval: 10 samples.
- Audio is converted to mono by channel averaging and resampled to 16 kHz when
  required.
- No noise reduction, speech enhancement, accent normalization, augmentation,
  manual transcript correction, or manual translation correction.
- Model loading and one warm-up inference are excluded from per-sample timing.
- Translation quality is intentionally calculated downstream rather than in
  the inference notebooks.

## Implemented evaluation dataset

The local frozen input is:

```text
data/final_sample/
├── final_sample_600_per_group.csv
└── final_sample_audio/              # 4,200 MP3 clips
```

`data/` is ignored by Git, so a fresh clone does not contain this dataset.
Only the de-identified `data/final_sample` material is in scope for repository
analysis.

### Provenance

- Speech, English transcripts, and accent metadata come from **Common Voice
  Scripted Speech 26.0 - English**.
- The dataset source is the [Mozilla Data Collective Common Voice
  release](https://mozilladatacollective.com/datasets/cmqim2hn800ssnr07gvmpcnwu).
- Simplified Chinese reference translations were extracted from CoVoST 2 and
  matched during data preparation before the de-identified final export.
- References are existing CoVoST 2 translations, not NLLB-generated targets.

The original sensitive Common Voice speaker identifier was replaced with a
regenerated pseudonymous identifier, `sample_id`. This is **pseudonymization /
de-identification**, not guaranteed anonymization: recordings from the same
speaker remain linkable through `sample_id`.

Never expose, reconstruct, or speculate about original identifier values or a
mapping to `sample_id`.

### Data preparation

[`01_data_preprocessing.ipynb`](notebooks/01_data_preprocessing.ipynb)
selects the first self-reported accent label, compares available target-language
references, and matches CoVoST 2 Chinese references through normalized English
sentence text. It filters duration outliers using the original five-group
pool's 1st–99th percentiles and excludes implausible transcript-length/audio-
duration combinations. It then adds England and United States English,
applies a 100-clip speaker cap, and samples 600 clips per group with seed 760.
The exported data retains regenerated speaker IDs and removes the source
speaker identifier.

Reference matching keeps the first CoVoST 2 translation for each normalized
sentence. Normalization can merge text variants, so the reference-matching
policy and reference quality remain limitations. Accent balance does not
match sentence content, recording conditions, or speaker counts across groups.
[`02_audio_extraction.ipynb`](notebooks/02_audio_extraction.ipynb) extracts the
selected recordings from the Common Voice archive; its paths and process-
priority setting currently target Windows and need adjustment elsewhere.

This is one frozen evaluation set. There is no project training/validation
split, model fitting, or hyperparameter search. Pilots test engineering
feasibility; the later decoding experiments are post-hoc diagnostics.

### Frozen dataset facts

| Property | Current value |
|---|---:|
| Evaluation clips | 4,200 |
| Accent groups | 7 |
| Clips per accent | 600 |
| Unique audio files | 4,200 |
| Pseudonymous speakers (`sample_id`) | 1,586 |
| Speakers contributing multiple clips | 579 |
| Maximum clips from one pseudonymous speaker | 88 |
| Total audio duration | 19,401.456 s (about 5.39 h) |
| Mean clip duration | 4.619 s |
| Clip-duration range | 1.728-9.384 s |
| Missing Chinese references | 0 |
| Distinct Chinese reference strings | 3,746 |

Equal clip counts make the dataset balanced by accent at the row level. They
do not make the clips statistically independent: speakers and sentence or
reference content can repeat. Speaker-aware and paired analysis is therefore
required.

### Accent groups

Each group contains exactly 600 clips:

1. England English
2. Filipino
3. Hong Kong English
4. India and South Asia (India, Pakistan, Sri Lanka)
5. Malaysian English
6. Southern African (South Africa, Zimbabwe, Namibia)
7. United States English

England English and United States English are the two groups added after the
five-group proposal.

### Metadata schema

The frozen CSV contains 21 columns:

```text
path, sentence_id, sentence, sentence_domain, up_votes, down_votes,
age, gender, accents, variant, locale, segment, primary_accent,
sentence_norm, clip, duration[ms], sentence_len_words,
max_plausible_words, sentence_len_chars, sample_id,
reference_translation_zh
```

Identifier semantics are important:

- `sample_id` is a regenerated pseudonymous **speaker identifier**. It can and
  does occur in multiple rows; it is not a clip key.
- `path` / `clip` identify the source audio within the frozen input.
- `sentence_id` identifies source content and may be shared by recordings.
- `id` is not present in the frozen CSV. The Direct and Cascaded notebooks add
  sequential values such as `sample_0001` to form a unique run-level clip key.
  That key is valid only while the frozen row order and metadata fingerprint
  are unchanged.

All three completed full inference runs recorded the same dataset fingerprints:

```text
metadata SHA-256:   57fb7e6b62647d661cb887bdd279f1b4af57bbf1fca8e5ee741b5490136dcdba
ordered id SHA-256: bf79323ce8acbf43a01d5dfb234b68b2e99fcb08d95671fd2bb2f9932c37f225
```

Use the generated `id` to align the two run outputs, and confirm the metadata
hash before relying on that alignment. Never use `sample_id` as a unique merge
key.

## Evaluation results

[`08_evaluation.ipynb`](notebooks/08_evaluation.ipynb) evaluates Direct,
Cascade-600M, and Cascade-3.3B against the same 4,200 Chinese references.
Its saved outputs and [merged_3system_with_metrics.csv](runs/evaluation_results/merged_3system_with_metrics.csv)
contain the three-system comparison. The scores below were previously checked
against the archived predictions using SacreBLEU 2.6.0. This documentation
update does not rerun model inference.

### Overall translation quality

Higher is better for all translation metrics in this table.

| System | Clips | Corpus BLEU (`zh`) | Corpus chrF | Corpus chrF++ | Mean sentence chrF++ |
|---|---:|---:|---:|---:|---:|
| Direct: SeamlessM4T v2-large | 4,200 | 38.86 | 32.38 | 25.08 | 27.86 |
| Cascade: Whisper large-v2 → NLLB-600M | 4,200 | 29.11 | 24.23 | 18.44 | 20.86 |
| Cascade: Whisper large-v2 → NLLB-3.3B | 4,200 | 31.91 | 26.36 | 20.06 | 22.87 |

Direct scores highest on this dataset, including within every accent group
under corpus BLEU and chrF++. NLLB-3.3B improves over the 600M cascade while
the separately executed Whisper runs produced matching transcript strings
for all 4,200 clips. These are comparisons of the
specified model systems, not evidence that one architecture is universally
better or that parameter count alone explains the difference.

BLEU uses `tokenize="zh"`. chrF and chrF++ use character order 6 and `beta=2`,
with word order 0 and 2 respectively, and default whitespace exclusion.
The chrF++ word component uses SacreBLEU's default word handling; the Chinese
BLEU tokenizer is not applied to chrF++. Report both character-based metrics
and keep their settings explicit.

**Corpus scores and mean sentence scores are different quantities.**
The statistical analysis uses per-clip chrF++, so its mean gaps and confidence
intervals must not be labelled as differences in corpus chrF++ or BLEU.

Normalized Whisper WER is **5.97% at corpus level**, versus **6.32% when
averaging per-clip WER**. Both cascades have the same WER because their
independently generated ASR transcript strings match in the archived outputs.
Normalization lowercases text, removes punctuation and collapses whitespace.
WER is an ASR diagnostic; Direct has no intermediate transcript to score.

### Statistical analysis

[`09_statistical_analysis.ipynb`](notebooks/09_statistical_analysis.ipynb)
implements paired, accent-stratified bootstrap analysis with seed 760,
1,000 resamples, and 95% percentile intervals. It reports speaker-cluster
resampling and clip-level sensitivity results, accent means and spreads,
Spearman associations, Kruskal–Wallis tests, Dunn comparisons with Holm
correction, and paired Wilcoxon tests at clip and speaker levels.

The tracked [`intervals_long.csv`](runs/statistical_analysis_results/intervals_long.csv)
reports these overall **mean sentence chrF++** gaps with speaker-clustered
intervals. Positive gaps favour the first named system.

| Paired comparison | Mean gap | 95% confidence interval |
|---|---:|---:|
| Direct − Cascade-600M | +7.00 | +6.45 to +7.60 |
| Direct − Cascade-3.3B | +4.99 | +4.39 to +5.70 |
| Cascade-3.3B − Cascade-600M | +2.01 | +1.61 to +2.42 |

Speaker-clustered Direct-minus-Cascade intervals are also positive within all
seven accents. The saved speaker-level Kruskal–Wallis tests show variation in
these gaps across accents (`p=0.0015` for 600M; `p=0.0087` for 3.3B), with
small reported effect sizes. However, the intervals for differences in
between-accent score spread include zero. These results support a system-score
advantage on this set, but do not establish that Direct is more accent-robust
under the spread measure. See
[`accent_means_ci.csv`](runs/statistical_analysis_results/accent_means_ci.csv) and
[`tests.csv`](runs/statistical_analysis_results/tests.csv).

The tracked [`spearman.csv`](runs/statistical_analysis_results/spearman.csv)
reports weak negative associations between normalized WER and cascade sentence
chrF++ (`rho=-0.188` for 600M; `rho=-0.196` for 3.3B). Higher WER is also
associated with a wider Direct-minus-Cascade gap. These are associations,
not proof of causal ASR-error propagation.

The statistical CSVs and notebook 09's retained execution output provide saved
evidence. The [statistical report](runs/statistical_analysis_results/09_statistical_analysis.pdf)
is also available. Speaker resampling accounts for repeated speakers, but not jointly
for repeated sentence content. Speaker-level rank tests use speaker means,
whereas the main bootstrap estimates remain weighted by clip counts.
Exploratory tests and their correction scope should be stated when reporting
findings. Notebook 09's execution reports calculation of `<unk>`-free intervals,
but its output file is absent from `runs/statistical_analysis_results/`.
Notebook 10 now supplies [subset intervals](runs/synthesis_results/intervals_unk_free.csv)
in the synthesis folder, with all three pairwise comparisons.

### Q1–Q9 synthesis and additional checks

Jidni's [10_synthesis_q1_q9.ipynb](notebooks/10_synthesis_q1_q9.ipynb) combines
the team's evaluation, statistical and diagnostic evidence into answers to
Q1–Q9. It adds common `<unk>`-free subset intervals, an ASR-error split, a
worst-clip audit, a Cascade-3.3B fallback check and a one-clip-per-speaker
sensitivity analysis. These calculations use existing predictions on CPU.

The [synthesis results](runs/synthesis_results/) contain seven CSVs, six saved
figures and a self-contained [dashboard](runs/synthesis_results/dashboard.html).
The [results README](runs/synthesis_results/README.md) explains the panels;
[READEME-synthesis.md](READEME-synthesis.md) explains dependencies, execution,
replay output paths and interpretation. These exploratory checks do not isolate
causal effects; selecting one clip per speaker is a sensitivity check on the
existing data, rather than a held-out evaluation on new data.

## Current project status

| Stage | Status | Evidence in repository |
|---|---|---|
| Research proposal | Tracked PDF available | [9_Proposal.pdf](presentation/9_Proposal.pdf) |
| Seven-group frozen sample | Complete locally; Git-ignored | `data/final_sample/` and preprocessing notebooks 01–02 |
| Seven-clip engineering pilot | Saved execution available | `create_pilot_samples.ipynb` |
| 35-clip hardware timing pilot | Archived feasibility results | `timing_test_pipelines.ipynb`, `runs/pilot_run_colab_tpu.zip` |
| Direct inference, 4,200 clips | 4,200/4,200 successful | `runs/direct_full_run_1788151795/` |
| Cascaded 600M inference, 4,200 clips | 4,200/4,200 successful | `runs/cascade_full_run_1788146589/` |
| Cascaded 3.3B inference, 4,200 clips | 4,200/4,200 successful | `runs/cascade_full_run_1790228071/` |
| Three-system WER and translation evaluation | Saved outputs and 4,200-row metric table available | Notebook 08, `runs/evaluation_results/08_evaluation.pdf`, `runs/evaluation_results/merged_3system_with_metrics.csv` |
| Confidence intervals and statistical tests | Saved notebook execution, report and four result CSVs; subset intervals supplied by notebook 10 | Notebook 09, [statistical_analysis_results/](runs/statistical_analysis_results/), [subset intervals](runs/synthesis_results/intervals_unk_free.csv) |
| Q1–Q9 synthesis and additional checks | Saved execution, seven CSVs, six figures and HTML dashboard available | Notebook 10, [synthesis_results/](runs/synthesis_results/) |
| Earlier Direct `<unk>` diagnostics | Full-run audit and two 35-clip sensitivity experiments archived | Notebooks 05–07 and investigation log |
| Further Direct `<unk>` analysis | Four notebooks, four scripts, and archived results available | `unk_analysis/` |
| Legacy two-system merge | Saved execution selects 600M; three-system evaluation loads 3.3B separately | `combine_translation_outputs.ipynb` |
| Literature survey | All thematic sections and group synthesis integrated | `literature_review/latex/` |
| Method/results presentation | Tracked PDF available | `presentation/9_MethodResults.pdf` |

The current work is interpretation, reproducibility checks, and final reporting.
Full evaluation and statistics are no longer missing stages.

## Notebooks

The evaluation, statistical and synthesis notebooks retain saved execution outputs.
The supplementary model-diagnostic notebooks provide code without retained
execution outputs; their separate results folders contain saved artifacts.
Review each notebook's configuration, paths, and archived results before
rerunning it.

| Notebook | Purpose | Expected working directory |
|---|---|---|
| [`01_data_preprocessing.ipynb`](notebooks/01_data_preprocessing.ipynb) | Prepares and samples the source data; requires local source datasets. | See [preprocessing guide](README-preprocessing.md) |
| [`02_audio_extraction.ipynb`](notebooks/02_audio_extraction.ipynb) | Extracts selected audio from the source archive. | See [preprocessing guide](README-preprocessing.md) |
| [`create_pilot_samples.ipynb`](notebooks/create_pilot_samples.ipynb) | Validates the frozen 7 x 600 dataset and creates a duration-varied, speaker-diverse pilot. The current code/output selects 1 clip per group (7 total). | Repository root or `notebooks/` |
| [`timing_test_pipelines.ipynb`](notebooks/timing_test_pipelines.ipynb) | Runs a 35-clip timing feasibility comparison and estimates full-run duration. It is not a translation-quality evaluation. | `notebooks/`; pilot paths under `data/timing_test_audio/` |
| [`03_direct_pipeline.ipynb`](notebooks/03_direct_pipeline.ipynb) | Runs frozen SeamlessM4T inference, checkpoints predictions, records timing/environment/configuration, and validates output integrity. | Repository root; `PROJECT_ROOT = Path.cwd()` |
| [`04_cascaded_pipeline.ipynb`](notebooks/04_cascaded_pipeline.ipynb) | Runs staged Whisper then NLLB inference with checkpointing, separate ASR/MT diagnostics, and final integrity checks. | Repository root; `PROJECT_ROOT = Path.cwd()` |
| [`combine_translation_outputs.ipynb`](notebooks/combine_translation_outputs.ipynb) | Validates identical run samples and shared metadata, then combines `asr_transcript`, `cascade_translation`, and `direct_translation` by unique `id`. It does not score them. | `notebooks/` |
| [`05_direct_unk_diagnostic.ipynb`](notebooks/05_direct_unk_diagnostic.ipynb) | Audits literal `<unk>` frequency, repeated content, and tokenizer behaviour. | Review notebook paths |
| [`06_direct_unk_sensitivity.ipynb`](notebooks/06_direct_unk_sensitivity.ipynb) | Tests greedy/beam-5 decoding and special-UNK suppression; saves generated token IDs and subset metrics. | Review notebook paths |
| [`07_direct_literal_unk_blocking_sensitivity.ipynb`](notebooks/07_direct_literal_unk_blocking_sensitivity.ipynb) | Tests blocking ordinary token sequences spelling `<unk>` and compares changed outputs. | Review notebook paths |
| [`08_evaluation.ipynb`](notebooks/08_evaluation.ipynb) | Computes normalized/raw WER, corpus and sentence translation metrics, accent tables, three-system gaps, and literal `<unk>` flags. | See [evaluation guide](README-evaluation.md); local replay inputs and outputs |
| [`09_statistical_analysis.ipynb`](notebooks/09_statistical_analysis.ipynb) | Paired speaker/clip bootstrap, accent comparisons, Spearman associations, and rank tests. | See [statistical guide](README-statistical-analysis.md); repository root |
| [`10_synthesis_q1_q9.ipynb`](notebooks/10_synthesis_q1_q9.ipynb) | Synthesises Q1–Q9, adds subset/fallback/worst-clip checks, and saves figures and an HTML dashboard. | See [synthesis guide](READEME-synthesis.md); repository root or `notebooks/` |
| [`copy_from_colab.ipynb`](notebooks/copy_from_colab.ipynb) | Colab helper that mounts Drive and archives `/content/runs`, `/content/outputs`, and `/content/results`. | Google Colab |

### Execution order for new inference

1. Follow [README-preprocessing.md](README-preprocessing.md) to prepare the
   metadata and extract the 4,200 audio clips under `data/final_sample/`,
   or provide the existing frozen inputs.
2. Run `create_pilot_samples.ipynb` and manually check the pilot.
3. Run `timing_test_pipelines.ipynb` if feasibility must be re-established on
   new hardware.
4. Run the Direct and Cascaded notebooks in pilot mode.
5. Freeze model revisions and decoding settings.
6. Run both pipelines with `DATASET_MODE = "final"`.
7. Preserve the run directories and their JSON fingerprints.
8. If a separate two-system merged dataset is needed, select the intended
   Cascaded run in `combine_translation_outputs.ipynb` (currently 600M) and run
   it from `notebooks/`. Notebook 08 can load the three prediction files directly.
9. Follow [README-evaluation.md](README-evaluation.md) for three-system scoring,
   then [README-statistical-analysis.md](README-statistical-analysis.md) for
   paired uncertainty and tests. Archived evaluation lives under
   `runs/evaluation_results/`; preserve replay outputs separately.
10. Follow [READEME-synthesis.md](READEME-synthesis.md) to combine the evidence
    in notebook 10 and regenerate the synthesis tables, figures and dashboard.

The completed full runs do not need to be repeated unless the frozen data,
models, decoding policy, or research design changes.

The combination notebook writes its validated 4,200-row output to
`data/full_translated_sample/full_translated_sample_metadata.csv`. This is a
local, Git-ignored downstream artifact; the tracked notebook records the
successful combination, while the model prediction CSVs in `runs/` remain the
reconstructable inputs.

The saved combination notebook still selects `cascade_full_run_1788146589`.
That legacy combined output uses NLLB 600M. Notebook 08 separately loads and
validates both cascades, so the tracked three-system metric table already
includes 3.3B and does not depend on updating the legacy merger.

## Reproducing the results

### Notebook replication entry points

The replication entry points are **notebooks**, with their code retained in
`.ipynb` files. Run notebook 08 for performance calculations, then notebook 09
for uncertainty and statistical comparisons. Notebook 10 then produces the
Q1–Q9 synthesis and its figures. No Python extraction is required.

| What to reproduce | Entry point | Running guide | Required resources |
|---|---|---|---|
| Dataset selection and audio extraction | Notebooks [01](notebooks/01_data_preprocessing.ipynb) and [02](notebooks/02_audio_extraction.ipynb) | [README-preprocessing.md](README-preprocessing.md) | Source metadata, CoVoST references and audio archive; CPU |
| Direct and Cascaded inference | Notebooks [03](notebooks/03_direct_pipeline.ipynb) and [04](notebooks/04_cascaded_pipeline.ipynb) | [README-running-pipelines.md](README-running-pipelines.md) | Frozen metadata/audio, model downloads and GPU |
| Translation-quality evaluation | [08_evaluation.ipynb](notebooks/08_evaluation.ipynb) | [README-evaluation.md](README-evaluation.md) | Archived prediction CSVs; CPU |
| Statistical comparisons | [09_statistical_analysis.ipynb](notebooks/09_statistical_analysis.ipynb) | [README-statistical-analysis.md](README-statistical-analysis.md) | Merged evaluation CSV; CPU |
| Q1–Q9 synthesis, figures and dashboard | [10_synthesis_q1_q9.ipynb](notebooks/10_synthesis_q1_q9.ipynb) | [READEME-synthesis.md](READEME-synthesis.md) | Archived evaluation, statistical and diagnostic results; CPU |
| Further `<unk>` experiments and summaries | [Supplementary notebooks and scripts](unk_analysis/) | [unk_analysis/README.md](unk_analysis/README.md) | Saved inputs for CPU summaries; GPU for model diagnostics |

### Recalculate the main results without inference

1. Open [README-evaluation.md](README-evaluation.md) and install its scoring
   dependencies in the notebook kernel. Use the three archived prediction CSVs
   as local inputs rather than mutable GitHub `main` URLs.
2. Configure a replay copy of notebook 08, restart the kernel, and execute its
   analysis cells in order through **FINAL CHECK + SAVE ANALYSIS DATAFRAME**.
   The guide identifies optional installation, GPU and export cells.
3. Check 4,200 unique clips, seven groups of 600, matching source/reference
   fields and the expected overall scores. The replay saves metric and table
   CSVs in a separate folder such as `tmp/evaluation_replay/`.
4. Follow [README-statistical-analysis.md](README-statistical-analysis.md),
   set notebook 09's `DATA_FILE` to the replay CSV, and choose a separate output
   directory. Restart its kernel and run the calculation cells and final
   `main()` invocation. Alternatively, analyse the archived
   [merged CSV](runs/evaluation_results/merged_3system_with_metrics.csv) directly.
5. Compare the generated tables with [evaluation evidence](runs/evaluation_results/)
   and [statistical evidence](runs/statistical_analysis_results/). Retain notebook
   09's generated `intervals_unk_free.csv`; notebook 10 supplies its own subset
   interval table in [synthesis_results/](runs/synthesis_results/).
6. Follow [READEME-synthesis.md](READEME-synthesis.md) for notebook 10. It can
   use the existing archive directly; select a separate output folder to
   regenerate its seven CSVs, six figures and dashboard without replacing them.
7. Save the executed replay notebooks and record inputs, dependency versions,
   metric signatures, seed and bootstrap count. Export PDFs separately if needed.

Audio and model weights are unnecessary for these three CPU stages. Current
notebooks require the configuration adjustments described in the guides; this
is not an unconfigured "Run All" workflow. Do not overwrite archived evidence
while checking a replay. Mean sentence chrF++ gaps and their intervals differ
from corpus translation-score gaps, and mean per-clip WER differs from corpus WER.

### Repeat model inference or further diagnostics

For a new inference run, provide the local frozen dataset and follow
[`README-running-pipelines.md`](README-running-pipelines.md) for Colab setup,
Drive transfer, pilot validation, full inference, resuming, and archiving.
Use the saved model revisions and keep new outputs in a new run directory.
The current Cascade notebook uses 3.3B; reproducing the historical 600M run
requires its model ID and resolved revision from the archived configuration.

For further `<unk>` analysis, follow [`unk_analysis/README.md`](unk_analysis/README.md).
Its saved-result summaries can run on CPU from the repository root:

```bash
python -m pip install numpy pandas scipy statsmodels matplotlib spacy wordfreq
python -m spacy download en_core_web_sm
python unk_analysis/scripts/accent_rate.py runs/evaluation_results/merged_3system_with_metrics.csv
python unk_analysis/scripts/word_type.py runs/evaluation_results/merged_3system_with_metrics.csv
python unk_analysis/scripts/decode_summary.py
python unk_analysis/scripts/trigger_words.py
```

The explicit metric-table arguments above account for its move into
`runs/evaluation_results/`; the supplementary scripts default to the
`runs/evaluation_results/merged_3system_with_metrics.csv` path. These scripts write into
`unk_analysis/results/`; preserve the archived files
or run in a separate checkout when comparing a replay. The four supplementary
notebooks rerun model-based diagnostics on Colab and have their own input,
Drive-path, smoke-test, and resume settings. Notebook 2 needs private audio;
the text-only, decoding-probability, and word-removal checks use text inputs.

## Completed run artifacts

### Summary

| Property | Direct | Cascade 600M baseline | Cascade 3.3B latest |
|---|---:|---:|---:|
| Local directory | `direct_full_run_1788151795` | `cascade_full_run_1788146589` | `cascade_full_run_1790228071` |
| Run date (UTC) | 2026-08-31 04:49–06:16 | 2026-08-31 03:23–04:33 | 2026-09-24 05:34–07:00 |
| Input / successful / failed | 4,200 / 4,200 / 0 | 4,200 / 4,200 / 0 | 4,200 / 4,200 / 0 |
| Total measured pipeline/stage-sum time | 3,898.567 s | 3,903.437 s | 4,650.148 s |
| Mean time per clip | 0.928 s | 0.929 s | 1.107 s |
| Median time per clip | 0.878 s | 0.902 s | 1.074 s |
| Mean real-time factor | 0.220 | 0.216 | 0.256 |
| Generation-limit flags | 0 | Whisper 0; NLLB 0 | Whisper 0; NLLB 0 |
| Peak allocated GPU memory | 2.876 GB | 3.159 GB | 11.126 GB |

These timings are computational diagnostics, not model-quality results. The
Direct value is measured around its per-sample pipeline. The Cascaded value is
the sum of separately measured Whisper and NLLB stages because the models were
run in separate passes. Neither includes model loading or warm-up, so these
columns should not be presented as a controlled serving-latency benchmark.

### Full-run environment

All three completed full runs record:

- Google Colab/Linux environment.
- Python 3.13.15.
- PyTorch 2.11.0+cu128 and torchaudio 2.11.0+cu128.
- Transformers 4.57.6.
- CUDA 12.8, FP16 inference, and an NVIDIA Tesla T4 (14.56 GB).
- GPU driver 580.82.07.

The JSON files record exact model revisions and dataset fingerprints, but
`git_commit` is `null` because the Colab execution did not run inside a Git
checkout. The stored output paths also retain their original `/content/...`
names even though the downloaded directories were renamed with `_full_run_`.

### Contents of each full-run directory

```text
runs/<system>_full_run_<timestamp>/
├── *_predictions.csv              # source metadata + model outputs
├── *_runtime.csv                  # per-sample runtime/status diagnostics
├── run_config.json                # frozen settings and dataset hashes
├── run_environment.json           # software/hardware/model revisions
├── run_summary.json               # completion and aggregate timing
├── runtime_per_clip.png
├── runtime_vs_audio_duration.png
└── 03_direct_pipeline.pdf or 04_cascaded_pipeline.pdf
```

The prediction schemas are:

```text
Direct:  original metadata + id + direct_translation
Cascade: original metadata + id + asr_transcript + cascade_translation
Combined target schema:
         original metadata + id + asr_transcript
         + cascade_translation + direct_translation
```

The tracked runtime CSVs contain a legacy `client_id` diagnostic column, but
it is blank for all 4,200 rows in all three completed full runs. Do not populate or
publish that field; `sample_id` is the only retained pseudonymous speaker
identifier.

### Timing-pilot archive

[`runs/pilot_run_colab_tpu.zip`](runs/pilot_run_colab_tpu.zip) contains both
TPU-labelled and Tesla-T4 GPU timing outputs for the 35-clip feasibility test,
including CSV/Parquet results, environment JSON, figures, HTML, and rendered
notebook PDFs. Treat these as pilot engineering measurements rather than final
quality evidence.

## Direct `<unk>` investigation

The original Direct run contains literal `<unk>` in **508/4,200 outputs
(12.10%)**, with 599 occurrences. The tracked follow-up artifacts are:

- [`direct_unk_diagnostic_1789953533`](runs/direct_unk_diagnostic_1789953533/): full-run frequency, accent/content associations, and tokenizer checks.
- [`direct_unk_sensitivity_1789954497`](runs/direct_unk_sensitivity_1789954497/): 35 originally affected clips, five per accent, tested with greedy and beam-5 decoding, with/without suppression of special UNK ID `1`.
- [`direct_literal_unk_blocking_1789970452`](runs/direct_literal_unk_blocking_1789970452/): the same subset tested with literal token-sequence constraints.

Generated-token inspection on the subset found ordinary tokens spelling the
marker, with no special UNK IDs. Suppressing ID `1` did not change greedy
outputs; beam-5 reduced exact-marker outputs only from 35 to 34. Blocking the
literal sequences removed exact `<unk>` strings but produced `<unk >` variants
in all 35 outputs. BLEU fell from 28.19 to 15.52 and chrF++ from 18.86 to 14.49;
this is not a successful repair.

These are post-hoc experiments on selected affected clips, run on CPU/FP32;
the baseline reproduced 33/35 original GPU/FP16 translations exactly. They do
not establish full-dataset effects or the model's internal cause. The official
4,200 Direct predictions remain unchanged. See the
[investigation log](SeamlessM4T_UNK_Investigation_Log.md) for evidence and limits.

### Further checks in `unk_analysis/`

The newer [`unk_analysis/`](unk_analysis/) work extends the earlier investigation
with text-only translation, a balanced 700-clip speech/special-token check,
decoding probabilities, word removal, and CPU analyses of accent and word type.

- Text input produces literal `<unk>` in **528/4,200 outputs (12.57%)**;
  88.4% of speech-affected clips are also affected with the reference English
  text. Audio is therefore not required to reproduce many affected outputs.
- In the 700-clip speech check, **74 clips (10.57%)** contain the hidden special
  UNK ID. This differs from the visible marker and from the earlier 35-clip
  subset, which had no special UNK IDs. The folder reports that these hidden
  tokens mostly concern punctuation at sentence ends.
- Sentence-level proper-noun presence has the same visible-marker rate in both
  groups (12.1%). Rarer content words show a stronger descriptive association:
  31.3% in the very-rare-word bin versus 5.1% in the common-word bin.
- The accent-only logistic model clustered by speaker reports `p=0.5006` for
  the joint accent terms. This does not establish equal rates, and concerns
  marker frequency rather than overall accent robustness.

These are post-hoc diagnostics. Text-based probability and word-removal tests
are not equivalent to speech-path tests, and word removal changes meaning.
Some narrative statistics in the supplementary README are not reproduced by
its four scripts; consult its limitations before reusing them. Neither the
hidden special token nor a proper-noun example proves the cause of the visible
marker. The original Direct predictions remain the benchmark output.

## Literature survey

The literature survey is a separate COMPSCI 760 deliverable organized as a
thematic IEEE conference paper rather than five disconnected paper summaries.

```text
literature_review/
├── assignment_instructions.md
├── team_plan.md
├── IEEE-conference-template-062824/   # local; ignored
├── member_1/ ... member_5/            # local notes/sources; ignored
└── latex/
    ├── main.tex
    ├── references.bib
    ├── README.md
    ├── .latexmkrc
    ├── figures/
    └── sections/
        ├── abstract.tex
        ├── introduction.tex
        ├── architectures.tex
        ├── accent_asr.tex
        ├── accent_st.tex
        ├── evaluation.tex
        ├── synthesis_gap.tex
        ├── conclusion.tex
        ├── author_contributions.tex
        └── ai_use_statement.tex
```

Current state:

- All thematic sections contain prose, including architectures, accent ASR,
  accent ST, and evaluation methodology.
- The abstract, introduction, cross-theme synthesis, conclusion, author
  contributions, and AI Use Statement are populated.
- The abstract describes a survey of 27 studies. The bibliography and integrated
  member contributions replace the earlier Member 1-only scaffold.
- LaTeX source is tracked; generated PDFs remain local and Git-ignored.

Build the survey with:

```bash
cd literature_review/latex
latexmk -pdf main.tex
```

`.latexmkrc` first searches the locally supplied official IEEE template. That
template directory and generated PDFs are ignored by Git, so a fresh clone
must provide `IEEEtran.cls` through the same local directory or a TeX
installation. See [`literature_review/latex/README.md`](literature_review/latex/README.md)
for ownership, length, terminology, and verification rules.

The assignment permits limited generative-AI assistance but requires each
author to locate, read, verify, and synthesize every paper they cite. The final
AI Use Statement must describe actual use accurately.

## Team-member contributions

The table summarises recorded project and literature-survey contributions.
Additional work can be added as it is completed; leave unknown names or
unrecorded contributions blank.

| Team member | Project contributions | Literature-survey contributions |
|---|---|---|
| Arizona Xing | Prepared the evaluation dataset and investigated Direct `<unk>` generation.<br><br><strong>Task 1: Dataset preparation</strong><ul><li>Matched Chinese references, filtered clips, capped speaker contributions, and sampled 600 clips per accent.</li><li>Extracted selected recordings and prepared the 35-clip timing subset.</li><li>Files:<ul><li>[01_data_preprocessing.ipynb](notebooks/01_data_preprocessing.ipynb)</li><li>[02_audio_extraction.ipynb](notebooks/02_audio_extraction.ipynb)</li></ul></li></ul><strong>Task 2: Further Direct `<unk>` analysis</strong><ul><li>Compared literal `<unk>` generation from English reference sentences and Whisper transcripts.</li><li>Inspected visible markers and hidden special UNK IDs in a balanced 700-clip speech sample.</li><li>Compared token probabilities, entropy, and alternative candidates at marker-generation steps.</li><li>Removed individual English words and compared influential words with controls.</li><li>Analysed trigger-word frequency and word class.</li><li>Analysed marker rates across accents with speaker-clustered uncertainty.</li><li>Examined associations with word frequency and proper-noun presence.</li><li>Files:<ul><li>[1_text_only_test.ipynb](unk_analysis/notebooks/1_text_only_test.ipynb)</li><li>[2_speech_special_token_check.ipynb](unk_analysis/notebooks/2_speech_special_token_check.ipynb)</li><li>[3_decode_probabilities.ipynb](unk_analysis/notebooks/3_decode_probabilities.ipynb)</li><li>[decode_summary.py](unk_analysis/scripts/decode_summary.py)</li><li>[4_word_removal.ipynb](unk_analysis/notebooks/4_word_removal.ipynb)</li><li>[trigger_words.py](unk_analysis/scripts/trigger_words.py)</li><li>[accent_rate.py](unk_analysis/scripts/accent_rate.py)</li><li>[word_type.py](unk_analysis/scripts/word_type.py)</li></ul></li><li>Results:<ul><li>[text_only/](unk_analysis/results/text_only/)</li><li>[special_token/](unk_analysis/results/special_token/)</li><li>[decode_probs/](unk_analysis/results/decode_probs/)</li><li>[word_removal/](unk_analysis/results/word_removal/)</li><li>[accent/](unk_analysis/results/accent/)</li><li>[word_type/](unk_analysis/results/word_type/)</li></ul></li></ul> | <ul><li>Reviewed Direct and Cascaded speech-translation architectures, ASR-to-MT error propagation, and system comparisons.</li><li>Drafted the Speech Translation Architectures and System Comparisons section.</li><li>Compared training resources and evaluation conditions across studies and designed the architecture comparison figure.</li></ul> |
| Zhitong Li | Performed statistical comparisons and maintained the shared metric table.<br><br><strong>Task 1: Statistical analysis and evaluation data</strong><ul><li>Implemented paired speaker/clip bootstrap intervals and accent-level comparisons.</li><li>Calculated Spearman associations between WER, translation quality, and system gaps.</li><li>Ran rank tests and produced confidence-interval, accent-mean, correlation, and test tables.</li><li>Updated the shared three-system metric table used by the statistical analysis.</li><li>Files:<ul><li>[09_statistical_analysis.ipynb](notebooks/09_statistical_analysis.ipynb)</li></ul></li><li>Results:<ul><li>[statistical_analysis_results/](runs/statistical_analysis_results/)</li><li>[intervals_long.csv](runs/statistical_analysis_results/intervals_long.csv)</li><li>[accent_means_ci.csv](runs/statistical_analysis_results/accent_means_ci.csv)</li><li>[spearman.csv](runs/statistical_analysis_results/spearman.csv)</li><li>[tests.csv](runs/statistical_analysis_results/tests.csv)</li><li>[merged_3system_with_metrics.csv](runs/evaluation_results/merged_3system_with_metrics.csv)</li></ul></li></ul> | <ul><li>Reviewed accent-related ASR performance, seen/unseen-accent generalisation, and mitigation.</li><li>Drafted the Accent Robustness in Speech Processing section.</li><li>Synthesised evidence on commercial ASR disparities, accent-specific codebooks, contrastive regularisation, and fairness-aware fine-tuning.</li></ul> |
| Nathan Naylin | Implemented and ran the translation pipelines, pilots, and earlier `<unk>` experiments.<br><br><strong>Task 1: Pipeline implementation and execution</strong><ul><li>Validated pilot selection and prepared a small engineering test set.</li><li>Measured Direct/Cascaded runtime and hardware feasibility on 35 clips.</li><li>Ran frozen SeamlessM4T on 4,200 clips with checkpointing, runtime logging, and output validation.</li><li>Ran staged Whisper → NLLB inference with both 600M and 3.3B translation models.</li><li>Validated and merged Direct/600M predictions by clip ID.</li><li>Created the Colab output-archiving helper.</li><li>Files:<ul><li>[create_pilot_samples.ipynb](notebooks/create_pilot_samples.ipynb)</li><li>[timing_test_pipelines.ipynb](notebooks/timing_test_pipelines.ipynb)</li><li>[03_direct_pipeline.ipynb](notebooks/03_direct_pipeline.ipynb)</li><li>[04_cascaded_pipeline.ipynb](notebooks/04_cascaded_pipeline.ipynb)</li><li>[combine_translation_outputs.ipynb](notebooks/combine_translation_outputs.ipynb)</li><li>[copy_from_colab.ipynb](notebooks/copy_from_colab.ipynb)</li></ul></li><li>Results:<ul><li>[pilot_run_colab_tpu.zip](runs/pilot_run_colab_tpu.zip)</li><li>[direct_full_run_1788151795/](runs/direct_full_run_1788151795/)</li><li>[cascade_full_run_1788146589/](runs/cascade_full_run_1788146589/)</li><li>[cascade_full_run_1790228071/](runs/cascade_full_run_1790228071/)</li></ul></li></ul><strong>Task 2: Earlier Direct `<unk>` investigation</strong><ul><li>Audited full-run marker frequency, accent/content patterns, and tokenizer behaviour.</li><li>Tested greedy/beam decoding and special-token suppression on 35 affected clips.</li><li>Tested literal-marker token constraints and compared changed outputs and quality scores.</li><li>Files:<ul><li>[05_direct_unk_diagnostic.ipynb](notebooks/05_direct_unk_diagnostic.ipynb)</li><li>[06_direct_unk_sensitivity.ipynb](notebooks/06_direct_unk_sensitivity.ipynb)</li><li>[07_direct_literal_unk_blocking_sensitivity.ipynb](notebooks/07_direct_literal_unk_blocking_sensitivity.ipynb)</li></ul></li><li>Results:<ul><li>[direct_unk_diagnostic_1789953533/](runs/direct_unk_diagnostic_1789953533/)</li><li>[direct_unk_sensitivity_1789954497/](runs/direct_unk_sensitivity_1789954497/)</li><li>[direct_literal_unk_blocking_1789970452/](runs/direct_literal_unk_blocking_1789970452/)</li></ul></li></ul><strong>Task 3: Project documentation</strong><ul><li>Documented project status, pipeline execution, and the earlier marker investigation.</li><li>Files:<ul><li>[README.md](README.md)</li><li>[README-running-pipelines.md](README-running-pipelines.md)</li><li>[SeamlessM4T_UNK_Investigation_Log.md](SeamlessM4T_UNK_Investigation_Log.md)</li></ul></li></ul> | <ul><li>Reviewed accent-labelled datasets, speech-translation data, and reference quality.</li><li>Drafted the dataset-design portion of Evaluation Data and Methodological Evidence.</li><li>Organised the survey and integrated member-authored sections.</li><li>Standardised terminology and formatting, removed duplication, and checked citations and rubric requirements.</li></ul> |
| Patricia Jennesha | Developed the quality-evaluation notebook and compared system performance by accent.<br><br><strong>Task 1: System and accent-level evaluation</strong><ul><li>Calculated raw/normalised WER, Chinese-tokenised BLEU, chrF, and chrF++.</li><li>Compared Direct/Cascaded translations and preserved the evaluation report and metric table.</li><li>Compared corpus and sentence-average translation scores across accent groups.</li><li>Compared WER and Direct/Cascade translation gaps by accent.</li><li>Files:<ul><li>[08_evaluation.ipynb](notebooks/08_evaluation.ipynb)</li></ul></li><li>Results:<ul><li>[evaluation_results/](runs/evaluation_results/)</li><li>[merged_3system_with_metrics.csv](runs/evaluation_results/merged_3system_with_metrics.csv)</li><li>[08_evaluation.pdf](runs/evaluation_results/08_evaluation.pdf)</li></ul></li></ul> | <ul><li>Reviewed ASR-error propagation, phonetic ASR errors, speech-model robustness, and accent-related downstream errors.</li><li>Drafted the Accent Robustness in Speech Translation section.</li><li>Assessed the relevance and limitations of existing evidence and the proposed gap in matched Direct/Cascaded evaluation.</li></ul> |
| Jidni Mayukh | Synthesised Q1–Q9 and produced additional checks, figures and a results dashboard.<br><br><strong>Task 1: Evidence synthesis and sensitivity analysis</strong><ul><li>Combined the team's evaluation, statistical and diagnostic results into evidence-backed answers to Q1–Q9.</li><li>Recomputed corpus metrics and produced paired-gap, accent-mean, subset and WER-association figures.</li><li>Calculated common &lt;unk&gt;-free subset intervals and compared zero-WER with positive-WER clips.</li><li>Audited the ten lowest-scoring clips per accent and system.</li><li>Checked Cascade-3.3B fallback on affected clips and one-clip-per-speaker sensitivity.</li><li>Built the self-contained HTML dashboard and its results README.</li><li>Files:<ul><li>[10_synthesis_q1_q9.ipynb](notebooks/10_synthesis_q1_q9.ipynb)</li></ul></li><li>Results:<ul><li>[synthesis_results/](runs/synthesis_results/)</li><li>[dashboard.html](runs/synthesis_results/dashboard.html)</li><li>[README.md](runs/synthesis_results/README.md)</li><li>[figures/](runs/synthesis_results/figures/)</li><li>[intervals_unk_free.csv](runs/synthesis_results/intervals_unk_free.csv)</li><li>[table_q5_scores_by_unk_subset.csv](runs/synthesis_results/table_q5_scores_by_unk_subset.csv)</li><li>[table_q6_scores_by_asr_error.csv](runs/synthesis_results/table_q6_scores_by_asr_error.csv)</li><li>[worst_clips_by_accent_system.csv](runs/synthesis_results/worst_clips_by_accent_system.csv)</li><li>[table_q8_worst_clip_summary.csv](runs/synthesis_results/table_q8_worst_clip_summary.csv)</li><li>[table_q9_fallback_check.csv](runs/synthesis_results/table_q9_fallback_check.csv)</li><li>[table_q9_one_clip_per_speaker.csv](runs/synthesis_results/table_q9_one_clip_per_speaker.csv)</li></ul></li></ul> | <ul><li>Reviewed translation metrics and statistical significance testing.</li><li>Drafted the Evaluation Metrics and Statistical Reliability and Controlled Evaluation subsections.</li><li>Covered WER, BLEU, chrF/chrF++, score comparability, paired comparisons, bootstrap uncertainty, and speaker/content dependence.</li></ul> |

Proposal role numbering and literature-survey role numbering differ. Use the
named contributions above and [`literature_review/team_plan.md`](literature_review/team_plan.md)
for the survey's division of work. Shared interpretation, presentation work,
and any additional contributions should be recorded by the team as they are
completed; Git history alone does not capture all collaborative work.



## Actual repository structure

```text
.
├── README.md
├── README-preprocessing.md
├── README-running-pipelines.md
├── README-evaluation.md
├── README-statistical-analysis.md
├── READEME-synthesis.md
├── SeamlessM4T_UNK_Investigation_Log.md
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_audio_extraction.ipynb
│   ├── create_pilot_samples.ipynb
│   ├── timing_test_pipelines.ipynb
│   ├── 03_direct_pipeline.ipynb
│   ├── 04_cascaded_pipeline.ipynb
│   ├── 05_direct_unk_diagnostic.ipynb
│   ├── 06_direct_unk_sensitivity.ipynb
│   ├── 07_direct_literal_unk_blocking_sensitivity.ipynb
│   ├── 08_evaluation.ipynb
│   ├── 09_statistical_analysis.ipynb
│   ├── 10_synthesis_q1_q9.ipynb
│   ├── combine_translation_outputs.ipynb
│   └── copy_from_colab.ipynb
├── runs/
│   ├── pilot_run_colab_tpu.zip
│   ├── direct_full_run_1788151795/
│   ├── cascade_full_run_1788146589/
│   ├── cascade_full_run_1790228071/
│   ├── direct_unk_diagnostic_1789953533/
│   ├── direct_unk_sensitivity_1789954497/
│   ├── direct_literal_unk_blocking_1789970452/
│   ├── evaluation_results/
│   │   ├── 08_evaluation.pdf
│   │   └── merged_3system_with_metrics.csv
│   ├── statistical_analysis_results/   # four CSVs, report PDF and method/Q3/Q4 notes
│   └── synthesis_results/              # seven CSVs, six figures, dashboard and README
├── unk_analysis/
│   ├── README.md
│   ├── notebooks/                     # four model-based diagnostics
│   ├── scripts/                       # four CPU analysis scripts
│   └── results/                       # CSVs, JSON records, and figures
├── presentation/
│   ├── 9_MethodResults.pdf            # tracked
│   ├── 9_Proposal.pdf                 # tracked
│   ├── update_1/                      # local drafts/notes; ignored
│   └── update_2/                      # local assignment instructions; ignored
├── data/                              # local; ignored
│   ├── final_sample/
│   ├── pilot_sample/
│   └── full_translated_sample/
└── literature_review/
    ├── assignment_instructions.md
    ├── team_plan.md
    ├── IEEE-conference-template-062824/  # local; ignored
    ├── member_1/ ... member_5/            # local; ignored
    └── latex/
```

There is no central `requirements.txt`, dependency lockfile, root `src/`, or
root test suite. Analysis scripts live under `unk_analysis/scripts/`; the
main inference/evaluation/statistics workflow is notebook-based.

The updated [.gitignore](.gitignore) allows presentation files outside
`presentation/update_1/` and `presentation/update_2/` to be tracked. Both
[9_Proposal.pdf](presentation/9_Proposal.pdf) and
[9_MethodResults.pdf](presentation/9_MethodResults.pdf) are tracked; the two
update directories remain ignored. Local datasets, source-paper notes, the
IEEE template, generated literature-survey PDFs, and presentation drafts in
those update directories are excluded from fresh clones.

## Environment and reproducibility

The model notebooks install their own dependencies, including Transformers,
PyTorch, torchaudio, pandas, NumPy, SentencePiece, Matplotlib, tqdm, psutil,
`huggingface_hub`, `hf_xet`, and `torchcodec`. Evaluation uses SacreBLEU and
jiwer; statistics uses SciPy; further diagnostics add statsmodels, spaCy, and
wordfreq. A CUDA GPU is strongly recommended for the large models.
Model downloads require substantial disk
space and access to Hugging Face.

There is no repository-wide locked environment. For an exact comparison with
the completed runs, use the versions and model commit SHAs recorded in each
run's `run_environment.json` and `run_config.json`. Preserve a new run in a new
directory rather than overwriting the completed artifacts.

## Limitations and remaining work

1. **Scope:** results concern these pretrained systems, seven self-reported
   accent groups, and English-to-Simplified-Chinese translation. Model families,
   training resources, capacity, and objectives differ; architecture and accent
   cannot be assigned sole causal responsibility for score differences.
2. **Speaker and content dependence:** 600 clips per accent does not mean 600
   independent speakers. The main bootstrap clusters speakers, but repeated
   sentences/references and recording conditions remain potential confounders.
   Clip-level tests should be treated as sensitivity analyses.
3. **Metric interpretation:** automatic scores use one reference per clip and
   do not establish human translation quality. Report corpus and sentence means
   separately, distinguish micro and macro WER, and record metric signatures.
   The main statistical intervals concern mean sentence chrF++, not corpus BLEU.
4. **Reproduction gaps:** notebook 09's installation cell has the `scip` typo,
   its introduction mentions a nonexistent standalone script, and
   its `intervals_unk_free.csv` is absent from the statistical results folder.
   Notebook 10 supplies subset intervals in the synthesis folder, with a
   different schema and all three pairwise comparisons.
   Notebook 08 uses mutable GitHub `main` URLs, writes to its current directory,
   and retains earlier narrative sections that predate later analysis. Its
   original proper-noun/vocabulary explanation is a hypothesis, not a verified
   mechanism. Some newer `<unk>` write-up statistics lack replication code.
   The supplementary scripts' default metric path also predates the folder move;
   use the explicit path shown in the reproduction commands.
5. **Legacy notebook wording:** the Direct notebook's introductory metadata
   notes call `sample_id` unique; current code uses it as a repeating speaker
   identifier. The pilot notebook describes a three-per-group default but is
   configured for one per group. The merge notebook still selects 600M even
   though the three-system evaluation already includes 3.3B.
6. **Provenance and access:** Colab full runs record model/data fingerprints but
   no Git commit SHA. Audio and several supporting documents are local-only;
   reproducible new inference requires the same frozen data and row order.
7. **Final reporting:** reconcile older presentation drafts with the current
   artifacts, record actual member contributions and feedback responses, and
   report the `<unk>` sensitivity work separately from the frozen benchmark.
   Preserve original predictions and do not report post-hoc decoding changes as
   a validated repair.

## Project work and external resources

The repository contains the team's data-preparation, inference-orchestration,
evaluation, statistical-analysis, and diagnostic code and resulting artifacts.
Pretrained SeamlessM4T, Whisper, and NLLB models, Common Voice recordings and
metadata, CoVoST 2 translation references, and library implementations are
external resources. The team did not train these models or author the source
dataset/reference translations.

Literature and metric references are recorded in
[`references.bib`](literature_review/latex/references.bib). The supplementary
[`unk_analysis/README.md`](unk_analysis/README.md) distinguishes its own results
from external context. The survey's
[AI Use Statement](literature_review/latex/sections/ai_use_statement.tex)
and supplementary README record AI assistance; claims and results remain the
responsibility of their contributors.

## Code documentation and submission coverage

The notebook running guides above identify inputs, configuration, execution
order, outputs, expected checks, recorded member contributions and external
resources. The existing team table records individual work; model training,
source datasets and third-party metric implementations are external resources.
When code is copied or adapted from an online example, record the original URL
and the changes beside that notebook cell. Contributor/source headers are not
consistently present in the current notebooks, so the table and guides do not
replace those cell-level credits.

| Requirement | Current evidence | Remaining documentation/code work |
|---|---|---|
| All experiments | Preprocessing, pilots, three full runs and notebooks 05–10; supplementary diagnostics | Some supplementary write-up calculations are listed as missing from the supplied code in [its limitations](unk_analysis/README.md#limitations) |
| Performance calculations | Notebook 08 scores WER, BLEU, chrF and chrF++; notebook 09 calculates uncertainty, tests and associations; notebook 10 adds synthesis and sensitivity checks | Preserve replay tables and distinguish notebook 09/10 subset-file schemas |
| Plotting | Inference/timing plots, notebook 08's displayed WER histogram, supplementary figures and six saved synthesis figures generated by notebook 10 | Save the standalone WER histogram if used; keep code and output for any additional reported figures |
| Replication instructions | Five root running guides and the supplementary README | Apply the documented configuration changes and verify the selected workflow from a fresh kernel |
| Contributions and online sources | Team-member table, guide attribution and external-resource sections | Credit copied/adapted snippets with actual source URLs; confirm ownership rather than inferring it |
| Meaningful file names and nonempty README files | Named notebooks and populated README files | Continue using descriptive names for new experiments and outputs |

This documentation update inspects notebook source, saved execution outputs and
result-file schemas. It does not execute preprocessing, inference, evaluation or
statistical analysis, and does not establish a fresh environment replay.
