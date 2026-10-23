# Zhitong Li: integration record and claim review

Integrated on 23 October 2026 from
[`member_4/zhitong_sections.tex`](member_4/zhitong_sections.tex) and
[`member_4/zhitong_references.bib`](member_4/zhitong_references.bib).
The original submission files remain unchanged.

## What was integrated

- Statistical Analysis into
  [`latex/sections/method_statistics_zhitong.tex`](latex/sections/method_statistics_zhitong.tex).
- Uncertainty, Accent Variation and ASR Associations, including both supplied
  tables, into
  [`latex/sections/results_statistics_zhitong.tex`](latex/sections/results_statistics_zhitong.tex).
- Six new references into the shared IEEE bibliography. The existing Koehn
  reference was retained once rather than duplicated. The original bibliography
  file was not edited.

The standalone document preamble, document environment and local bibliography
commands were omitted because the main report already supplies them. The two
section headings became subsections to fit the existing Methodology and Results
structure. All labels were retained.

The only prose correction was **“Robustness is operationalization as” →
“Robustness is operationalized as.”** No numerical results, interpretations,
equations, table contents, first-person wording or other member-authored prose
were rewritten. No unrelated report source files were changed.

## Claim requiring author review — left unchanged

The opening of **Accent means and spread** says:

> Accent moves each system far less than system choice does.

This is too broad if “system choice” includes all three pairwise comparisons.
The overall Cascade-3.3B minus Cascade-600M mean sentence chrF++ gap is
**2.01 points**, while the two cascades' between-accent spreads are **2.70** and
**3.17 points**. The claim is therefore not supported as a universal comparison
between every system gap and every accent spread. The larger Direct–Cascade
gaps, **7.00** and **4.99**, do support a narrower comparison of those particular
point estimates.

Also, the study observes accent-group associations; it does not experimentally
establish how much accent causes a system's score to change. This is an
interpretation/scope concern, not an incorrect table cell. The submitted wording
has been preserved for the author to review.

Evidence:

- [`intervals_long.csv`](../runs/statistical_analysis_results/intervals_long.csv):
  speaker-unit overall `mean_gap` rows and `spread_max_minus_min` rows.
- Original claim: `member_4/zhitong_sections.tex`, line 72.

## Verified against saved evidence

No numerical discrepancy was found in the following checks:

- Every numeric cell in both supplied tables matches the labelled speaker-unit
  rows in `intervals_long.csv` and
  [`accent_means_ci.csv`](../runs/statistical_analysis_results/accent_means_ci.csv),
  after the displayed rounding.
- The overall paired gaps, per-accent Direct gaps, 3.3B lift intervals, system
  spreads and spread-difference intervals match the saved tables. Spread
  **differences** are stored in `accent_means_ci.csv`, not `intervals_long.csv`.
- The quoted speaker-level Kruskal–Wallis results, Wilcoxon results for England
  and Hong Kong, positive rank-biserial ranges, significant Dunn–Holm pair
  counts and accent-order correlations agree with
  [`tests.csv`](../runs/statistical_analysis_results/tests.csv).
- All 32 speaker-bootstrap WER-association intervals in
  [`spearman.csv`](../runs/statistical_analysis_results/spearman.csv) exclude zero,
  as stated. Their reported overall correlations and intervals agree with the
  saved rows.

The statistical notebook source was inspected to check resampling/test
descriptions. Notebooks, inference and statistical resampling were not rerun.
These checks establish agreement with the archived implementation/results, not
an independent validation of every statistical assumption.

The Liu–Peng blockwise-bootstrap, Dror et al. and Card et al. reference titles
and author metadata were checked against their primary publication pages:
[Liu and Peng](https://arxiv.org/abs/1912.09508),
[Dror et al.](https://aclanthology.org/P18-1128/), and
[Card et al.](https://aclanthology.org/2020.emnlp-main.745/).
No substantive claim or bibliography entry was changed as a result.
