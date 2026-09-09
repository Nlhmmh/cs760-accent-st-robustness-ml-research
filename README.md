# Regional English Accent Robustness in Speech Translation

COMPSCI 760 research project comparing how regional English accents are
associated with the translation quality of Direct and Cascaded
speech-to-text translation systems.

The repository contains the original Group 9 proposal, the frozen-model
inference notebooks, completed Direct and Cascaded run artifacts, and an IEEE
LaTeX literature survey in progress. The implemented experiment has advanced
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
team roles are recorded in [`9_Proposal.pdf`](9_Proposal.pdf). This README
documents the current implemented state when it differs from that proposal.

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
                                    | NLLB-200 distilled 600M       |
                                    | English-to-Chinese MT         |
                                    +---------------+---------------+
                                                    |
                                                    v
                                           Cascaded Chinese text

Direct text and Cascaded text ------> same CoVoST 2 Chinese reference
                                      planned: chrF++ / BLEU
Whisper transcript -----------------> Common Voice English transcript
                                      planned: WER diagnostic
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
- MT: `facebook/nllb-200-distilled-600M`.
- NLLB language direction: `eng_Latn` to `zho_Hans`.
- Frozen revisions resolved by the completed run:
  - Whisper: `ae4642769ce2ad8fc292556ccea8e901f1530655`.
  - NLLB: `f8d333a098d19b4fd9a8b18f94170487ad3f821d`.
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

The two completed inference runs recorded the same dataset fingerprints:

```text
metadata SHA-256:   57fb7e6b62647d661cb887bdd279f1b4af57bbf1fca8e5ee741b5490136dcdba
ordered id SHA-256: bf79323ce8acbf43a01d5dfb234b68b2e99fcb08d95671fd2bb2f9932c37f225
```

Use the generated `id` to align the two run outputs, and confirm the metadata
hash before relying on that alignment. Never use `sample_id` as a unique merge
key.

## Evaluation and statistical-analysis plan

Inference is complete, but the quality and statistical analyses are not yet
implemented in this repository.

### Planned measures

- **chrF++ (primary):** final Chinese translation quality for both systems.
- **BLEU (secondary):** complementary translation score and comparability with
  prior speech-translation work.
- **WER (Cascaded diagnostic only):** Whisper ASR output against the Common
  Voice English transcript. WER is not a translation metric.
- **Direct-Cascade gap:** paired per-clip difference, with the sign and metric
  direction stated explicitly.

### Planned comparisons

- Overall Direct versus Cascaded translation quality.
- Within-accent paired Direct versus Cascaded differences.
- Between-accent variation in each pipeline.
- Whether the Direct-Cascade gap varies by accent group.
- Paired confidence intervals or significance tests for system differences.
- Association between Whisper WER and Cascaded translation quality or
  degradation.

Because `sample_id` repeats, uncertainty estimates should account for
speaker-level clustering, or explicitly justify any clip-level resampling
assumption. Repeated sentence/reference content should also be reported or
controlled. Association between WER and translation scores must not be
described as proof of causal error propagation.

No translation-quality scores, accent-robustness findings, confidence
intervals, or hypothesis-test results should be inferred from the runtime
artifacts.

## Current project status

| Stage | Status | Evidence in repository |
|---|---|---|
| Research proposal | Complete | `9_Proposal.pdf` |
| Seven-group frozen sample | Complete locally; Git-ignored | `data/final_sample/` |
| Seven-clip engineering pilot | Complete | Executed `create_pilot_samples.ipynb` |
| 35-clip hardware timing pilot | Complete | Notebook plus archived TPU/T4 artifacts |
| Direct inference, 4,200 clips | Complete; 4,200/4,200 successful | `runs/direct_full_run_1788151795/` |
| Cascaded inference, 4,200 clips | Complete; 4,200/4,200 successful | `runs/cascade_full_run_1788146589/` |
| Direct/Cascade output combination | Notebook executed and validated | `combine_translation_outputs.ipynb` |
| WER, chrF++, and BLEU calculation | **Not present** | Evaluation notebook still required |
| Confidence intervals / statistical tests | **Not present** | Statistical-analysis notebook still required |
| Accent-level interpretation | **Not started in tracked artifacts** | Depends on verified metrics/statistics |
| Literature survey | In progress | IEEE LaTeX scaffold; Member 1 portion populated |

## Notebooks

The notebooks contain saved outputs from their latest executions. They are
workflow records as well as executable code, so review the configuration cell
before rerunning one.

| Notebook | Purpose | Expected working directory |
|---|---|---|
| [`create_pilot_samples.ipynb`](notebooks/create_pilot_samples.ipynb) | Validates the frozen 7 x 600 dataset and creates a duration-varied, speaker-diverse pilot. The current code/output selects 1 clip per group (7 total). | Repository root or `notebooks/` |
| [`timing_test_pipelines.ipynb`](notebooks/timing_test_pipelines.ipynb) | Runs a 35-clip timing feasibility comparison and estimates full-run duration. It is not a translation-quality evaluation. | Repository root / Colab project root |
| [`03_direct_pipeline.ipynb`](notebooks/03_direct_pipeline.ipynb) | Runs frozen SeamlessM4T inference, checkpoints predictions, records timing/environment/configuration, and validates output integrity. | Repository root; `PROJECT_ROOT = Path.cwd()` |
| [`04_cascaded_pipeline.ipynb`](notebooks/04_cascaded_pipeline.ipynb) | Runs staged Whisper then NLLB inference with checkpointing, separate ASR/MT diagnostics, and final integrity checks. | Repository root; `PROJECT_ROOT = Path.cwd()` |
| [`combine_translation_outputs.ipynb`](notebooks/combine_translation_outputs.ipynb) | Validates identical run samples and shared metadata, then combines `asr_transcript`, `cascade_translation`, and `direct_translation` by unique `id`. It does not score them. | `notebooks/` |
| [`copy_from_colab.ipynb`](notebooks/copy_from_colab.ipynb) | Colab helper that mounts Drive and archives `/content/runs`, `/content/outputs`, and `/content/results`. | Google Colab |

### Recommended execution order

1. Put the de-identified metadata and 4,200 audio clips under
   `data/final_sample/`.
2. Run `create_pilot_samples.ipynb` and manually check the pilot.
3. Run `timing_test_pipelines.ipynb` if feasibility must be re-established on
   new hardware.
4. Run the Direct and Cascaded notebooks in pilot mode.
5. Freeze model revisions and decoding settings.
6. Run both pipelines with `DATASET_MODE = "final"`.
7. Preserve the run directories and their JSON fingerprints.
8. Run `combine_translation_outputs.ipynb` from `notebooks/`.
9. Implement and run the missing evaluation and statistical-analysis stages.

The completed full runs do not need to be repeated unless the frozen data,
models, decoding policy, or research design changes.

The combination notebook writes its validated 4,200-row output to
`data/full_translated_sample/full_translated_sample_metadata.csv`. This is a
local, Git-ignored downstream artifact; the tracked notebook records the
successful combination, while the model prediction CSVs in `runs/` remain the
reconstructable inputs.

## Completed run artifacts

### Summary

| Property | Direct full run | Cascaded full run |
|---|---:|---:|
| Local directory | `direct_full_run_1788151795` | `cascade_full_run_1788146589` |
| Run date (UTC) | 2026-08-31 04:49-06:16 | 2026-08-31 03:23-04:33 |
| Input / successful / failed | 4,200 / 4,200 / 0 | 4,200 / 4,200 / 0 |
| Total measured pipeline/stage-sum time | 3,898.567 s | 3,903.437 s |
| Mean time per clip | 0.928 s | 0.929 s |
| Median time per clip | 0.878 s | 0.902 s |
| Mean real-time factor | 0.220 | 0.216 |
| Generation-limit flags | 0 | Whisper 0; NLLB 0 |
| Peak allocated GPU memory | 2.876 GB | 3.159 GB |

These timings are computational diagnostics, not model-quality results. The
Direct value is measured around its per-sample pipeline. The Cascaded value is
the sum of separately measured Whisper and NLLB stages because the models were
run in separate passes. Neither includes model loading or warm-up, so the two
columns should not be presented as a controlled serving-latency benchmark.

### Full-run environment

Both completed runs record:

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
it is blank for all 4,200 rows in both completed runs. Do not populate or
publish that field; `sample_id` is the only retained pseudonymous speaker
identifier.

### Timing-pilot archive

[`runs/pilot_run_colab_tpu.zip`](runs/pilot_run_colab_tpu.zip) contains both
TPU-labelled and Tesla-T4 GPU timing outputs for the 35-clip feasibility test,
including CSV/Parquet results, environment JSON, figures, HTML, and rendered
notebook PDFs. Treat these as pilot engineering measurements rather than final
quality evidence.

## Literature survey

The literature survey is a separate COMPSCI 760 deliverable organized as a
thematic IEEE conference paper rather than five disconnected paper summaries.

```text
literature_review/
├── assignment_instructions.md
├── team_plan.md
├── IEEE-conference-template-062824/   # local official template; ignored
├── member_1/                          # local notes/sources; ignored
└── latex/
    ├── main.tex
    ├── references.bib
    ├── README.md
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

- Title, authors, terminology, report structure, collaboration placeholders,
  Author Contributions, and AI Use Statement are scaffolded.
- Member 1's dataset/reference-quality synthesis is populated in
  `sections/evaluation.tex`.
- Three Member 1 references are present: Common Voice, CoVoST 2, and the
  MCV_ACCENT/codebook paper.
- Sections owned by Members 2-5 and the group-level abstract, synthesis, and
  conclusion still contain placeholders.
- The current local PDF is a three-page working draft, not the final survey.

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

## Team

The proposal records these project-execution responsibilities:

| Team member | Proposal responsibility |
|---|---|
| Arizona Xing | Dataset preparation and balanced evaluation-set construction |
| Zhitong Li | Dataset support, accent-ASR literature, and final interpretation |
| Nathan Naylin | Direct/Cascaded pipelines and architecture literature |
| Patricia Jennesha | WER, chrF++, BLEU, and accent-level evaluation |
| Jidni Mayukh | Association analysis and system-gap statistical analysis |

All members share progress review, interpretation, report writing,
presentation preparation, and final checking. Literature-survey ownership uses
a different member numbering and division; follow
[`literature_review/team_plan.md`](literature_review/team_plan.md) for that
deliverable.

## Actual repository structure

```text
.
├── 9_Proposal.pdf
├── README.md
├── notebooks/
│   ├── create_pilot_samples.ipynb
│   ├── timing_test_pipelines.ipynb
│   ├── 03_direct_pipeline.ipynb
│   ├── 04_cascaded_pipeline.ipynb
│   ├── combine_translation_outputs.ipynb
│   └── copy_from_colab.ipynb
├── runs/
│   ├── pilot_run_colab_tpu.zip
│   ├── direct_full_run_1788151795/
│   └── cascade_full_run_1788146589/
├── data/                              # local and Git-ignored
│   └── final_sample/
└── literature_review/
    ├── assignment_instructions.md
    ├── team_plan.md
    ├── IEEE-conference-template-062824/  # local and ignored
    ├── member_1/                         # local and ignored
    └── latex/
```

The repository currently has no `src/`, `configs/`, `scripts/`, `tests/`,
central `requirements.txt`, or dependency lockfile. Do not rely on paths for
those components unless they are added later.

## Environment and reproducibility

The model notebooks install their own dependencies, including Transformers,
PyTorch, torchaudio, pandas, NumPy, SentencePiece, Matplotlib, tqdm, psutil,
`huggingface_hub`, `hf_xet`, and `torchcodec`. A CUDA GPU is strongly
recommended for the large models. Model downloads require substantial disk
space and access to Hugging Face.

There is no repository-wide locked environment. For an exact comparison with
the completed runs, use the versions and model commit SHAs recorded in each
run's `run_environment.json` and `run_config.json`. Preserve a new run in a new
directory rather than overwriting the completed artifacts.

## Known inconsistencies and next work

1. **Proposal versus implementation:** the proposal's 5 x 600 design was
   expanded to the implemented 7 x 600 design. Use 4,200, not 3,000, for all
   current analysis and reporting.
2. **Missing evaluation stage:** no tracked notebook currently computes WER,
   chrF++, BLEU, uncertainty, statistical tests, or the WER/translation-score
   association.
3. **Identifier wording:** old markdown in the Direct notebook says
   `sample_id` is unique. The data and current code show that it is a repeating
   speaker identifier. The generated `id` is the unique clip-level pairing
   key.
4. **Pilot documentation:** `create_pilot_samples.ipynb` describes a three-per-
   group default in markdown, but its current configuration and saved output
   use one per group.
5. **Git provenance:** the completed Colab run records have exact model and
   data fingerprints but no Git commit SHA.
6. **Local-only data products:** the frozen sample, combined translation file,
   Member 1 source PDFs/notes, IEEE template, and generated LaTeX PDF are
   ignored and will not appear in a fresh clone.
7. **Literature draft:** Member 1's section is integrated, but the survey still
   requires the other members' verified reading and the group-level synthesis.

The immediate research milestone is to implement a reproducible evaluation
notebook on the combined 4,200-row output, followed by speaker-aware paired
statistical analysis and accent-level interpretation.
