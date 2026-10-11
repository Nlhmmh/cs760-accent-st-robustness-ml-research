# Synthesis results: Q1 to Q9

This folder is written by `notebooks/10_synthesis_q1_q9.ipynb` (Jidni Mayukh). The notebook answers the nine research questions from the 1 October action plan using files already tracked in the repository, and adds a small number of CPU-only checks. No model is rerun.

## dashboard.html

Open it in any browser. It is one self-contained file (figures are embedded), so it works from a local clone or a GitHub download without a network connection.

What it shows, top to bottom:

1. **Headline numbers.** Direct's lead over each cascade and the 3.3B-over-600M lift, all as mean sentence chrF++ with speaker-clustered 95% intervals from `runs/statistical_analysis_results/intervals_long.csv` (Zhitong); the count of Direct outputs containing literal `<unk>` and the mean Whisper WER from `runs/evaluation_results/merged_3system_with_metrics.csv` (Patricia's notebook 08, building on Jidni's base evaluation; committed by Nathan, speaker column added by Zhitong).
2. **One panel per question, Q1 to Q9.** Each panel has the question, a one-sentence answer, and where a figure helps, the figure from the notebook:
   - Q1: corpus BLEU, chrF, chrF++ and mean sentence chrF++ for the three systems (`figures/q1_overall_scores.png`).
   - Q2: the three pairwise gaps in every accent with intervals (`figures/q2_per_accent_gaps.png`).
   - Q3: accent means per system with intervals (`figures/q3_accent_means.png`).
   - Q5: corpus chrF++ on all clips, on the 3,692 `<unk>`-free clips and on the 508 affected clips (`figures/q5_unk_subsets.png`).
   - Q6: Whisper WER by accent, and Spearman rho between WER and cascade quality or the Direct gap, by accent (`figures/q6_wer_and_spearman.png`).
   - Q7: the 3.3B-minus-600M lift in every accent against the overall interval (`figures/q7_scale_lift.png`).
   - Q4, Q8 and Q9 are text panels; their evidence is tabular and lives in the notebook.
3. **Contributions.** Which team member produced the inputs each answer rests on.
4. **Footer.** Metric settings, bootstrap settings and the standing caveat that every finding is an association on this frozen set.

## Other files in this folder

| File | What it is | New or copied |
|---|---|---|
| `intervals_unk_free.csv` | Paired speaker-clustered gap intervals on the 3,692 clips where Direct did not write `<unk>`; same resampler, seed and resample count as notebook 09, checked to reproduce its tracked overall intervals exactly | New (notebook 09's code writes this file, but it was never tracked) |
| `worst_clips_by_accent_system.csv` | The ten lowest-scoring clips per accent per system with source, transcript, all three outputs and the reference | New |
| `table_q5_scores_by_unk_subset.csv` | All three systems scored on the full set, the `<unk>`-free subset and the affected subset | New |
| `table_q6_scores_by_asr_error.csv` | Mean sentence chrF++ by whether Whisper made any word error on the clip | New |
| `table_q8_worst_clip_summary.csv` | What the worst-ten sets have in common (zero scores, `<unk>`, WER, reference length) | New |
| `table_q9_fallback_check.csv` | Corpus scores if Cascade-3.3B replaced Direct on the 508 `<unk>` clips | New |
| `table_q9_one_clip_per_speaker.csv` | Gap intervals on a one-clip-per-speaker sample (1,586 clips, seed 760) | New |
| `figures/*.png` | The six figures above | New |

## How to regenerate

Open the notebook in Google Colab or Jupyter and run all cells. On Colab the first cell clones the repository; locally, run from the repository root or from `notebooks/`. The notebook installs sacrebleu pinned to 2.6.0 (the version in the main README's reproduction instructions) and tabulate. The run takes a few minutes on CPU.

## Reading the numbers

- Corpus scores and mean sentence scores are different quantities; intervals are on mean sentence chrF++.
- A gap is the first named system minus the second. Positive favours the first.
- Speaker (`sample_id`) is the default resampling unit because speakers repeat (1,586 speakers, up to 88 clips each). Clip-level intervals are a sensitivity check.
- The systems differ in family, size and training data, so no finding assigns a single cause to architecture or accent.
