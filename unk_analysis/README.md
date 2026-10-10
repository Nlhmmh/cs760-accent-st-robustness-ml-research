# `<unk>` analysis: why does the Direct system write `<unk>`?

In our evaluation, the Direct system (SeamlessM4T v2-large) writes the literal string `<unk>` in 508 of the 4,200 Chinese translations (12.1%). The cascades never do. This folder contains a set of post-hoc checks that try to find out what the `<unk>` is linked to. **The original 4,200 Direct predictions are not changed by anything here.**

## Where this fits, and where to find the earlier steps

This analysis comes after the earlier `<unk>` investigation (PR #14). That work is not copied or modified here; it stays where it is.

| Step | What | Where to find it |
|---|---|---|
| 1 | Evaluation set (4,200 clips, 7 accent groups) | `../notebooks/01_data_preprocessing.ipynb`, `02_audio_extraction.ipynb`. The metadata (`final_sample_600_per_group.csv`) and the audio are kept locally and are not in the repository. |
| 2 | Direct and Cascade predictions | `../notebooks/03_direct_pipeline.ipynb`, `04_cascaded_pipeline.ipynb`; outputs in `../runs/direct_full_run_1788151795/`, `cascade_full_run_1788146589/` and `cascade_full_run_1790228071/` |
| 3 | Evaluation table (metrics, `direct_has_unk` flag) | `../notebooks/08_evaluation.ipynb`; the table is `../runs/merged_3system_with_metrics.csv` |
| 4 | Earlier `<unk>` investigation | `../SeamlessM4T_UNK_Investigation_Log.md`; `../notebooks/05_direct_unk_diagnostic.ipynb`, `06_direct_unk_sensitivity.ipynb`, `07_direct_literal_unk_blocking_sensitivity.ipynb`; `../runs/direct_unk_diagnostic_*`, `direct_unk_sensitivity_*`, `direct_literal_unk_blocking_*` |
| 5 | **This folder**: further checks on what `<unk>` is linked to | see below |

## Main findings

| Question | Finding |
|---|---|
| Does accent matter? | `<unk>` rate is 10.3% to 13.5% across the seven accents; the intervals overlap (test p about 0.5). No evidence of an accent effect, but small differences cannot be ruled out (about 70% power for a 5-point difference). |
| What kind of sentences? | Rate is 31.3% when the rarest content word is very rare and 5.1% when all words are common. Sentences with and without a proper noun: 12.1% vs 12.1%. |
| Does it need audio? | Not necessarily. Giving the same model the English **text** gives 12.6% (528 of 4,200), and 88% of the clips that fail with speech also fail with text. This supports a role for the text translation/generation process; the exact mechanism is not known (59 clips fail only with speech, 79 only with text). |
| Is it hidden by our decoding? | The decoder removes the model's special unknown token. It appears in 10.6% of speech clips (700-clip sample), but almost always at the end of the sentence (73 of the 74 clips), replacing the Chinese full stop or quote marks in the cases checked (no dropped words were found). The 508 count stands. |
| Is the vocabulary missing characters? | Among the characters in the reference translations, the tokenizer cannot write `。 “ ” 、 — ’ 《 》` and 29 rare characters. 18 of the 508 visible `<unk>` (3.5%) are in sentences whose reference contains one of the rare characters; this is co-occurrence, not a proven cause. |
| How sure is the model when it writes `<unk>`? | Less sure than at other Chinese-character steps (probability 0.60 vs 0.73). The runner-up is within 10 times of the winner in 72% of cases vs 44%. Sentences without `<unk>` give `<` almost no probability. |
| Which English word triggers it? | Removing the most influential word makes `<unk>` disappear in 80.5% of the 385 sentences (310), against 9.9% (38) when a random other word is removed. When the random word is a content word (161 sentences, the fairer comparison), it is 78.3% (126) against 13.0% (21). Triggers are mostly ordinary nouns of medium frequency and a few interjections ("Oh"); proper nouns are only modestly over-represented. |

All of these are descriptive. They show what `<unk>` is associated with, not a proven cause.

## What each part does

| # | Question | Method | Notebook / script | Results |
|---|---|---|---|---|
| A | Accent and `<unk>` rate | Rate per accent with speaker-level bootstrap intervals (seed 760, 1,000 resamples); logistic regression with sentence length | `scripts/accent_rate.py` | `results/accent/` |
| B | Rare words, proper nouns | `<unk>` rate by rarest-word frequency (wordfreq), spaCy tags and sentence length; logistic regression clustered by sentence | `scripts/word_type.py` | `results/word_type/` |
| 1 | Does it need audio? | Same model, same pinned revision, English text as input (reference sentence and Whisper transcript) | `notebooks/1_text_only_test.ipynb` | `results/text_only/` |
| 2 | Is it hidden by our decoding? | Re-run Direct on a balanced 700-clip sample keeping special tokens; reproduction check against the original outputs | `notebooks/2_speech_special_token_check.ipynb` | `results/special_token/` |
| 3 | How sure is the model? | Probability, entropy and top-5 candidates at every step, for `<unk>` sentences and length-matched controls | `notebooks/3_decode_probabilities.ipynb`, `scripts/decode_summary.py` | `results/decode_probs/` |
| 4 | Which word triggers it? | Remove one English word at a time, re-score the `<unk>` step, re-translate; random-word control; word frequency and word class of the triggers | `notebooks/4_word_removal.ipynb`, `scripts/trigger_words.py` | `results/word_removal/` |

Each results folder holds the output CSV files and the figure (`.png`) where there is one. The four Colab steps (`text_only`, `special_token`, `decode_probs`, `word_removal`) also hold the `run_summary_*.json` of the run (model revision, decoding settings, device, counts). In the decode-probabilities summary JSON, `other_steps_p_chosen_median` is the first-look baseline (all other steps of the original `unk` group, about 0.79), not the final comparison (0.73) in `unk_decode_probs_summary.csv`.

## Folder layout

```
unk_analysis/
├── README.md
├── notebooks/     # 1 to 4: need a GPU (run on Google Colab, T4)
├── scripts/       # A, B and the summaries of 3 and 4: run on a normal computer
└── results/       # accent/, word_type/, text_only/, special_token/, decode_probs/, word_removal/
```

## How to reproduce

**Inputs**
- `merged_3system_with_metrics.csv`: the three-system evaluation table from the evaluation notebook. It is in the repository as `../runs/merged_3system_with_metrics.csv`, which is where the scripts look by default; you can also pass its path as the first argument.
- `../runs/direct_full_run_1788151795/direct_predictions.csv` (in this repository): speaker ids for part A.
- Notebook 2 also needs `final_sample_600_per_group.csv` and `final_sample_audio.zip`. The audio is kept private and is not in the repository.

**Order**
1. `python scripts/accent_rate.py`
2. `python scripts/word_type.py`
3. Run `notebooks/1_text_only_test.ipynb` on Colab (T4). Copy its outputs into `results/text_only/`.
4. Run `notebooks/2_speech_special_token_check.ipynb` on Colab. It writes to `MyDrive/cs760/special_unk_check/` on Drive; copy the outputs into `results/special_token/`.
5. Run `notebooks/3_decode_probabilities.ipynb` on Colab. Copy `decode_steps.csv` and `decode_sentences.csv` into `results/decode_probs/`, then `python scripts/decode_summary.py`.
6. Run `notebooks/4_word_removal.ipynb` on Colab. Copy `occlusion_sentences.csv` and `occlusion_words.csv` into `results/word_removal/`, then `python scripts/trigger_words.py`.

Notebook 1 reads `merged_3system_with_metrics.csv` from its working folder on Colab and writes its results to a local `runs/` folder there; download them afterwards. Notebooks 2 to 4 read their inputs from a Google Drive folder (`MyDrive/cs760` by default; see the first code cell) and write their results to subfolders of it. Notebooks 2 to 4 have a 20-minute time budget, save as they go, resume after a disconnect and release the GPU at the end. Notebooks 1, 3 and 4 have a `SMOKE` switch for a quick test (in notebooks 3 and 4, smoke runs write to separate files); notebook 2 checks the first 8 clips against the original outputs before it continues.

**Environment:** Python 3, pandas, numpy, scipy, statsmodels, matplotlib, spaCy with `en_core_web_sm`, wordfreq (scripts); transformers 4.x, sentencepiece, sacrebleu, torch (notebooks, installed by the first cell). Model: `facebook/seamless-m4t-v2-large`, revision `5f8cc790b19fc3f67a61c105133b20b34e3dcb76`, greedy decoding, `max_new_tokens=256`, target `cmn`, FP16 on a Colab T4 (the same settings as the main Direct run).

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
- The four scripts reproduce the tables and figures in `results/` from the inputs. Many numbers quoted in the write-up come from calculations that are not in these scripts (for example the power figures, the sentence-level tables, and the per-sentence maxima of the decoding probabilities). The full tokenizer scan, some additional regressions and the proper-noun bootstrap interval were also computed outside these scripts and are not reproduced by them. The same holds for the paired 61% / 67% sentence comparison and the position figures for the decoding probabilities, the de-duplicated sentence table, the rank correlation 0.85, the accent p-value and the 82 / 52 table of the text-only test, the position and punctuation shares of the hidden token, and the outcome bins by size of the probability drop and the counts of sentences with one or more high-impact words in the word-removal test. (The word-removal rates, intervals and McNemar tests are produced by `scripts/trigger_words.py` and saved in `results/word_removal/unk_trigger_summary.csv`.) The tokenizer scan covered the distinct characters of the reference translations only (2,644), not the whole vocabulary.
- The word-removal notebook resets its random generator when it resumes after a disconnect, so the random-word control is not guaranteed to be identical between an uninterrupted run and a resumed one. The saved results match an uninterrupted replay.
- The decoding-probability comparison uses all other Chinese-character steps in the sentences that wrote `<unk>`; these steps are not matched for word frequency, position or word class.

## AI assistance

The code, analysis and this README were developed with the help of an AI assistant. The author ran the notebooks, checked the outputs and is responsible for the content.
