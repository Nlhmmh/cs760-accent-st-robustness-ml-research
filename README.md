# CS760 Accent ST Robustness ML Research

Research project for **COMPSCI 760 – Advanced Topics in Machine Learning**.

This project investigates how **regional English accents affect the translation quality of Direct and Cascaded speech-to-text translation systems**.

## Research Question

> **How does regional English accent affect the translation quality of direct and cascaded speech-to-text translation systems?**

## Project Overview

The project evaluates two established speech-translation architectures across multiple regional English accent groups.

### Direct Speech Translation

```text
English Speech
    ↓
SeamlessM4T v2-large
    ↓
Target Translation
```

### Cascaded Speech Translation

```text
English Speech
    ↓
Whisper large-v2
    ↓
English Transcript
    ↓
NLLB-200 distilled 600M
    ↓
Target Translation
```

These systems are used as **benchmark/reference systems** based on prior speech-translation research.

The project does **not** aim to develop a new model. Instead, it evaluates how existing Direct and Cascaded systems respond to regional English accent variation.

---

## Dataset

The experiment combines:

- **Mozilla Common Voice Scripted Speech 26.0 – English**
  - English speech recordings
  - source transcripts
  - speaker/accent metadata

- **CoVoST2**
  - human-translated speech-translation references
  - used as the ground-truth target translation

### Selected Accent Groups

The core evaluation uses five regional English accent groups:

1. India & South Asia
2. Southern African
3. Filipino
4. Malaysian English
5. Hong Kong English

### Evaluation Set

- **600 clips per accent group**
- **5 accent groups**
- **3,000 clips total**

The dataset is balanced across accent groups.

Preprocessing includes:

- valid audio/reference filtering
- CoVoST2 reference matching
- duration filtering
- speaker contribution control
- balanced sampling with a fixed random seed

---

## Evaluation

### Translation Metrics

- **chrF++** — primary translation metric
- **BLEU** — secondary translation metric

Both Direct and Cascaded outputs are evaluated against the same human CoVoST2 reference translations.

### ASR Diagnostic

For the Cascaded system:

- Whisper transcripts are compared against Common Voice reference transcripts.
- **Word Error Rate (WER)** is calculated.

WER is used as a diagnostic to investigate whether ASR errors are associated with downstream translation degradation.

---

## Statistical Analysis

The project will analyse:

- Direct vs. Cascaded translation performance
- performance differences across accent groups
- Direct–Cascade performance gaps
- paired bootstrap confidence intervals
- statistical significance of system differences
- relationship between Whisper WER and Cascaded translation quality

The analysis focuses on **associations and observed performance differences**, not strict causal claims.

---

## Repository Structure

```text
cs760-accent-st-robustness-ml-research/
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── .gitignore
├── .env.example
│
├── configs/
│   ├── base.yaml
│   └── experiments/
│       └── zh_5accents_600.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── manifests/
│
├── notebooks/
│   ├── 01_dataset_audit.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_direct_pipeline.ipynb
│   ├── 04_cascaded_pipeline.ipynb
│   ├── 05_evaluation.ipynb
│   ├── 06_statistical_analysis.ipynb
│   └── 07_results_visualisation.ipynb
│
├── src/
│   ├── data/
│   ├── pipelines/
│   ├── evaluation/
│   ├── analysis/
│   └── utils/
│
├── outputs/
│   ├── predictions/
│   ├── metrics/
│   └── logs/
│
├── results/
│   ├── statistical_tests/
│   ├── tables/
│   └── figures/
│
├── scripts/
└── tests/
```

---

## Experimental Workflow

```text
Common Voice + CoVoST2
          ↓
     Data Audit
          ↓
     Preprocessing
          ↓
Balanced Evaluation Set
  5 × 600 = 3,000 clips
          ↓
   ┌──────┴──────┐
   ↓             ↓
 Direct        Cascade
SeamlessM4T    Whisper
   ↓             ↓
Translation   Transcript
                 ↓
                NLLB
                 ↓
             Translation
   └──────┬──────┘
          ↓
      Evaluation
   chrF++ / BLEU / WER
          ↓
  Statistical Analysis
          ↓
 Accent-Group Comparison
          ↓
 Tables / Figures / Findings
```

---

## Main Pipeline Artifacts

### Evaluation Manifest

```text
data/manifests/evaluation_manifest_v1.parquet
```

Contains the exact samples used in the experiment.

Example fields:

```text
sample_id
audio_path
speaker_id
accent
sentence_id
source_text
reference_translation
target_language
audio_duration_sec
```

### Direct Predictions

```text
outputs/predictions/direct_predictions.parquet
```

### ASR Predictions

```text
outputs/predictions/asr_predictions.parquet
```

### Cascaded Predictions

```text
outputs/predictions/cascade_predictions.parquet
```

### Evaluation Metrics

```text
outputs/metrics/sample_metrics.parquet
```

Example fields:

```text
sample_id
accent
wer
direct_chrf
cascade_chrf
direct_bleu
cascade_bleu
chrf_gap
bleu_gap
```

---

## Reproducibility

Experiment settings are stored in YAML configuration files.

Example:

```yaml
experiment:
  name: zh_5accents_600
  seed: 42

dataset:
  samples_per_accent: 600
  max_clips_per_speaker: 100

models:
  direct: facebook/seamless-m4t-v2-large
  asr: openai/whisper-large-v2
  mt: facebook/nllb-200-distilled-600M

evaluation:
  metrics:
    - chrf++
    - bleu
    - wer
```

Important reproducibility principles:

- use a fixed random seed
- keep raw data unchanged
- version evaluation manifests
- record exact model identifiers
- save intermediate predictions
- keep experiment configurations under Git
- do not overwrite finalized evaluation datasets

---

## Prototype Strategy

Before running the full 3,000-sample experiment:

1. verify dataset loading
2. create a small pilot dataset
3. run Direct ST on the pilot
4. run Cascaded ST on the same pilot
5. calculate WER, chrF++, and BLEU
6. verify statistical-analysis code
7. freeze the full evaluation manifest
8. run the complete experiment

The goal is to verify the complete pipeline on a small subset before expensive full-scale inference.

---

## Team Responsibilities

- **Member 1** — Dataset preparation
- **Member 2** — Dataset support, accent-robustness literature review, final interpretation
- **Member 3** — Direct and Cascaded ST pipelines, Direct-vs-Cascade literature review
- **Member 4** — Evaluation metrics
- **Member 5** — Statistical analysis

All members contribute to:

- weekly progress reviews
- result interpretation
- report writing
- presentation preparation
- Q&A

---

## Key References

- Robinson et al. (2024). *JHU IWSLT 2024 Dialectal and Low-resource System Description.*
- Prabhu et al. (2023). *Accented Speech Recognition With Accent-specific Codebooks.*
- Wang et al. (2021). *CoVoST 2 and Massively Multilingual Speech Translation.*
- Ardila et al. (2020). *Common Voice: A Massively-Multilingual Speech Corpus.*
- Popović (2017). *chrF++: Words Helping Character n-grams.*
- Papineni et al. (2002). *BLEU: A Method for Automatic Evaluation of Machine Translation.*

---

## Research Scope

This repository focuses on:

- regional English accent robustness
- Direct vs. Cascaded speech translation
- balanced accent-level evaluation
- human-reference translation evaluation
- ASR error diagnostics
- statistical comparison of system performance

It does **not** currently focus on:

- training a new speech-translation architecture
- accent-specific model adaptation
- large-scale model fine-tuning
- synthetic translation references

---

## Status

**Current stage:** Repository setup and dataset preprocessing.

Planned next milestone:

> Build and validate the frozen **3,000-sample evaluation manifest** before running the full Direct and Cascaded pipelines.
