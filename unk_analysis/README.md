# `<unk>` analysis: why does the Direct system write `<unk>`?

In our evaluation, the Direct system (SeamlessM4T v2-large) writes the literal string `<unk>` in 508 of the 4,200 Chinese translations (12.1%). Neither archived cascade run contains the visible marker. This folder contains post-hoc checks of what the marker is associated with. **The original 4,200 Direct predictions are not changed by anything here.**

## Where this fits, and where to find the earlier steps

This analysis comes after the earlier `<unk>` investigation (PR #14). That work is not copied or modified here; it stays where it is.

| Step | What | Where to find it |
|---|---|---|
| 1 | Evaluation set (4,200 clips, 7 accent groups) | `../notebooks/01_data_preprocessing.ipynb`, `02_audio_extraction.ipynb`. Frozen metadata is tracked at `../data/final_sample/final_sample_600_per_group.csv`; recordings remain outside the repository. |
| 2 | Direct and Cascade predictions | `../notebooks/03_direct_pipeline.ipynb`, `04_cascaded_pipeline.ipynb`; outputs in `../runs/direct_full_run_1788151795/`, `cascade_full_run_1788146589/` and `cascade_full_run_1790228071/` |
| 3 | Evaluation table (metrics, `direct_has_unk` flag) | `../notebooks/08_evaluation.ipynb`; the table is `../runs/evaluation_results/merged_3system_with_metrics.csv` |
| 4 | Earlier `<unk>` investigation | `../SeamlessM4T_UNK_Investigation_Log.md`; `../notebooks/05_direct_unk_diagnostic.ipynb`, `06_direct_unk_sensitivity.ipynb`, `07_direct_literal_unk_blocking_sensitivity.ipynb`; `../runs/direct_unk_diagnostic_*`, `direct_unk_sensitivity_*`, `direct_literal_unk_blocking_*` |
| 5 | **This folder**: further checks on what `<unk>` is linked to | see below |

## Main findings

| Question | Finding |
|---|---|
| Is marker presence associated with accent? | Rates range from 10.3% to 13.5% across the seven groups. The speaker-clustered joint logistic-regression test did not detect an association (p = 0.50); sentence clustering and length adjustment give p = 0.45 and 0.48. These results do not establish equivalence. Of 370 normalized sentences recorded more than once, six have mixed marker status. Of 52 cross-accent repeated sentences marked at least once, 46 are marked in every recording; these counts are descriptive. |
| What kind of sentences? | Rate is 31.3% when the minimum content-lemma Zipf frequency is at most 2.5 and 5.1% in the bin above 4, which includes 48 clips assigned the median (4.12) because they lack a content token. Content tokens are alphabetic spaCy NOUN, VERB, ADJ or ADV tokens, excluding PROPN; frequencies use lower-cased lemmas. The length-adjusted OR is 0.52 per Zipf unit. Clips with and without a proper noun both have a 12.1% marker rate; the OR adjusted for length and rarest-lemma frequency is 0.95 [0.75, 1.21]. |
| Does it need audio? | The marker is not exclusive to speech input. Reference-transcript input gives 528 of 4,200 marked outputs (12.6%) and reproduces the marker in 449 of 508 speech-marked clips (88.4%). There are 59 speech-only and 79 text-only marked clips. Text input bypasses the speech encoder, so recurrence does not locate the cause in the speech pathway. |
| Is it hidden by our decoding? | Special UNK ID 1, which decoding removes, occurs in 74 of 700 re-run speech outputs (10.6%); none of these has the visible marker. ID 1 is the penultimate generated token in 73 of the 74 clips, and none of the 74 decoded outputs ends in Unicode punctuation. This does not establish whether ID 1 replaced punctuation. The archived count of 508 and the marker-free subset are defined by the visible string, not by special-token IDs. |
| Is the vocabulary missing characters? | Among the characters in the reference translations, the tokenizer cannot write `。 “ ” 、 — ’ 《 》` and 29 rare characters. 18 of the 508 clips with visibly marked Direct outputs (3.5%) are in sentences whose reference contains one of the rare characters; this is co-occurrence, not a proven cause. |
| How sure is the model when it writes `<unk>`? | In the text-input diagnostic sample, the median model-assigned probability of the generated token was 0.60 at the 472 marker-start steps, versus 0.73 at other Chinese-character steps in the same 392 sentences. At the marker-start steps, the second most probable token was within a factor of 10 of the chosen one in 72% of cases, versus 44% at those other steps. In the length-matched control sentences that produced no marker, the marker-start tokens received little probability at any step (figure from `scripts/decode_summary.py`). These are next-token probabilities, not probabilities of the whole marker or measures of translation quality. |
| What does word removal show? | The selected word maximizes the local reduction in combined marker-start probability at the first marker step with the decoder prefix fixed. Removing it makes the marker disappear in 310 of 385 sentences (80.5%), versus 38 (9.9%) after random-other-word deletion. When the random word is not a spaCy stop word (161 sentences), the rates are 78.3% (126) versus 13.0% (21). Pooled selected words have lower surface-form Zipf frequency than other non-stop words (medians 3.8 versus 4.6), and 57.1% are common nouns versus 44.5% of the comparison words (PROPN counted separately). Targeted selection and changes in source meaning prevent a causal interpretation of rarity or a claim of improved translation. |

All of these are descriptive. They show what `<unk>` is associated with, not a proven cause.

## What each part does

| # | Question | Method | Notebook / script | Results |
|---|---|---|---|---|
| A | Accent and `<unk>` rate | Rate per accent with speaker-level bootstrap intervals (seed 760, 1,000 resamples); logistic regression with sentence length | `scripts/accent_rate.py` | `results/accent/` |
| Data | Label multiplicity and gender-label balance | Counts from frozen clip metadata; male-label proportions by accent group | `scripts/dataset_summary.py` | `results/data/` |
| Data | Reference spot-check | One author's manual judgments of 20 English sentence–Chinese reference pairs sampled at clip level (seed 760): sentence match, translation judgement (`ok` / `minor` / `wrong`) and notes | Manual review | `results/data/reference_spotcheck_20_seed760.csv` |
| B | Rare words, proper nouns | `<unk>` rate by rarest-word frequency (wordfreq), spaCy tags and sentence length; logistic regression clustered by sentence | `scripts/word_type.py` | `results/word_type/` |
| 1 | Does it need audio? | Same model and pinned revision with English text input; summary also groups archived speech-marker status by original and normalized sentence | `notebooks/1_text_only_test.ipynb`, `scripts/modality_summary.py` | `results/text_only/` |
| 2 | Is it hidden by our decoding? | Re-run Direct on a balanced 700-clip sample keeping special tokens; compare strings, stored token positions and decoded ending punctuation | `notebooks/2_speech_special_token_check.ipynb`, `scripts/modality_summary.py` | `results/special_token/` |
| 3 | How sure is the model? | Probability, entropy and top-5 candidates at every step, for `<unk>` sentences and length-matched controls | `notebooks/3_decode_probabilities.ipynb`, `scripts/decode_summary.py` | `results/decode_probs/` |
| 4 | What does word removal show? | Delete each whitespace-delimited word, re-score the first marker step, select the largest local probability reduction and re-translate; random-word control | `notebooks/4_word_removal.ipynb`, `scripts/trigger_words.py` | `results/word_removal/` |

Each results folder holds the output CSV files and the figure (`.png`) where there is one. The four Colab steps (`text_only`, `special_token`, `decode_probs`, `word_removal`) also hold the `run_summary_*.json` of the run (model revision, decoding settings, device, counts). In the decode-probabilities summary JSON, `other_steps_p_chosen_median` is the first-look baseline (all other steps of the original `unk` group, about 0.79), not the final comparison (0.73) in `unk_decode_probs_summary.csv`.

## Folder layout

```
unk_analysis/
├── README.md
├── notebooks/     # 1 to 4: need a GPU (run on Google Colab, T4)
├── scripts/       # A, B and the summaries of 1 to 4: run on a normal computer
└── results/       # data/, accent/, word_type/, text_only/, special_token/, decode_probs/, word_removal/
```

## How to reproduce

**Inputs**
- `merged_3system_with_metrics.csv`: the three-system evaluation table from the evaluation notebook. It is in the repository as `../runs/evaluation_results/merged_3system_with_metrics.csv`, which is where the scripts look by default; you can also pass its path as the first argument.
- `../runs/direct_full_run_1788151795/direct_predictions.csv` (in this repository): speaker ids for part A.
- Notebook 2 also needs the tracked `../data/final_sample/final_sample_600_per_group.csv` and a separately supplied `final_sample_audio.zip`. The recordings are not in the repository; copy the CSV and audio archive to the notebook's configured input folder.

**Order**
0. `python scripts/dataset_summary.py` (or pass the frozen metadata path).
1. `python scripts/accent_rate.py`
2. `python scripts/word_type.py`
3. Run `notebooks/1_text_only_test.ipynb` on Colab (T4). Copy its outputs into `results/text_only/`.
4. Run `notebooks/2_speech_special_token_check.ipynb` on Colab. It writes to `MyDrive/cs760/special_unk_check/` on Drive; copy the outputs into `results/special_token/`, then `python scripts/modality_summary.py` (counts for steps 1 and 2, sentence consistency, hidden-token positions and punctuation). Sentence normalization strips and lower-cases the text, collapses whitespace and removes characters outside `\w` and `\s`, matching the preprocessing notebook. Ending punctuation means the last non-whitespace character has a Unicode category starting with `P`; this definition does not establish whether ID 1 replaced punctuation.
5. Run `notebooks/3_decode_probabilities.ipynb` on Colab. Copy `decode_steps.csv` and `decode_sentences.csv` into `results/decode_probs/`, then `python scripts/decode_summary.py`.
6. Run `notebooks/4_word_removal.ipynb` on Colab. Copy `occlusion_sentences.csv` and `occlusion_words.csv` into `results/word_removal/`, then `python scripts/trigger_words.py`.

Notebook 1 reads `merged_3system_with_metrics.csv` from its working folder on Colab and writes its results to a local `runs/` folder there; download them afterwards. Notebooks 2 to 4 read their inputs from a Google Drive folder (`MyDrive/cs760` by default; see the first code cell) and write their results to subfolders of it. Notebooks 2 to 4 have a 20-minute time budget, save as they go, resume after a disconnect and release the GPU at the end. Notebooks 1, 3 and 4 have a `SMOKE` switch for a quick test (in notebooks 3 and 4, smoke runs write to separate files); notebook 2 checks the first 8 clips against the original outputs before it continues.

**Environment:** Python 3, pandas, numpy, scipy, statsmodels, matplotlib, spaCy with `en_core_web_sm`, wordfreq (scripts); transformers 4.x, sentencepiece, sacrebleu, torch (notebooks, installed by the first cell). Model: `facebook/seamless-m4t-v2-large`, revision `5f8cc790b19fc3f67a61c105133b20b34e3dcb76`, greedy decoding, `max_new_tokens=256`, target `cmn`, FP16 on a Colab T4 (the same settings as the main Direct run).

Exact library versions for the original diagnostic runs were not recorded. The local review replay used spaCy 3.8.14, `en_core_web_sm` 3.8.0, wordfreq 3.1.1 and statsmodels 0.14.5; its `unk_wordtype_rates.csv` and `unk_wordtype_logit.csv` matched the archived files byte for byte. These are replay versions, not evidence of the original Colab environment.

## What is ours and what comes from elsewhere

**Our work:** all code and results in this folder (notebooks, scripts, tables, figures).

**External sources used for context or comparison (not our results):**
- Seamless Communication et al., "SeamlessM4T: Massively Multilingual & Multimodal Machine Translation," arXiv:2308.11596, 2023. We use its statement that the original NLLB-200 vocabulary lacked many Chinese characters.
- Meta, `facebookresearch/seamless_communication`, `src/seamless_communication/cli/m4t/finetune/trainer.py`. The default `label_smoothing = 0.2` is cited only as a consistent explanation for the probability ceiling near 0.8. We could not find the setting used for the released checkpoint in the public sources we checked.
- GitHub issue #168 in the same repository ("Outputs too many `<unk>` symbols with Mandarin Chinese"): other users report the same behaviour in text-only translation; there is no official explanation.
- Libraries: Hugging Face transformers, sacrebleu (M. Post, 2018), spaCy, wordfreq, statsmodels, scipy. The chrF++ setting is the one from M. Popovic (2017).

## Limitations

- The probability and word-removal tests use text input, not audio. The text-only test (1) shows that text reproduces the problem, but it is not the same as the speech path.
- Removing a word changes the meaning; the word-removal test shows what the model reacts to, not a fix and not a proof of cause.
- One model, one decoding setting, post-hoc analysis, and several exploratory tests without multiple-comparison correction.
- The probability ceiling near 0.8 is consistent with label smoothing, but this is not confirmed for the released model.
- Word frequency comes from a general word list, and word classes from an automatic tagger.
- Clips share speakers and sentences, and each analysis adjusts for at most one of them: the accent-rate bootstrap resamples speakers, the accent regression is run once clustered by speaker and once by sentence, the word-type regression clusters by sentence, and the decoding-probability and trigger-word bootstraps resample sentences. The word-level Fisher test in `trigger_words.py` and the Wilson intervals (for example the 700-clip special-token sample) adjust for neither, and the accent test on the 700-clip sample is clustered by sentence only (clustering by speaker gives a larger p-value). Intervals and p-values are therefore approximate.
- The scripts reproduce their named summary tables and figures from saved inputs; they do not reproduce every exploratory calculation. The full tokenizer scan, some additional regressions and the proper-noun bootstrap interval remain outside these scripts. So do the paired 61% / 67% decoding-probability comparison, per-sentence maxima and position figures, the text-only rank correlation 0.85, its accent p-value and 82 / 52 table, and word-removal outcome bins by probability drop and counts of sentences with high-impact words. The modality counts, repeated-sentence consistency and hidden-ID position/punctuation counts are now produced by `scripts/modality_summary.py`; metadata counts are produced by `scripts/dataset_summary.py`. Word-removal rates, intervals, pooled word statistics and McNemar tests are saved by `scripts/trigger_words.py` in `results/word_removal/unk_trigger_summary.csv`. The tokenizer scan covered distinct characters in reference translations only (2,644), not the whole vocabulary.
- The word-removal notebook resets its random generator when it resumes after a disconnect, so the random-word control is not guaranteed to be identical between an uninterrupted run and a resumed one. The saved results match an uninterrupted replay.
- The decoding-probability comparison uses all other Chinese-character steps in the sentences that wrote `<unk>`; these steps are not matched for word frequency, position or word class.

## AI assistance

The code, analysis and this README were developed with the help of an AI assistant. The author ran the notebooks, checked the outputs and is responsible for the content.
