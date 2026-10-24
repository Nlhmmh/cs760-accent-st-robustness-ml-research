# Group 9 IEEE final report

This is the integrated final-report source. Read
[the report plan](../report_plan.md) and [the assignment instructions](../instructions.md)
before writing. Section ownership follows named project contributions in
[the root README](../../README.md#team-member-contributions). Nathan is the organizer.

The layout follows `literature_review/latex/main.tex`: IEEEtran conference
format, five authors, member section inputs, a shared BibTeX file and `.latexmkrc`.
The class is resolved from the existing supplied IEEE template; that directory
must remain available. The final report has its own bibliography and sections,
so editing it does not change the literature survey.

## Build

From this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

This produces the review preview `main.pdf`.
Generated PDFs and auxiliary files are ignored by Git.

Build the submission-named copy after checking the paper:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=9_FinalReport main.tex
```

This produces the required `9_FinalReport.pdf`.
Run `latexmk -c main.tex` to clean auxiliary files while keeping the PDF.
For the named build, use `latexmk -c -jobname=9_FinalReport main.tex`.

## Files to edit

All files below are in `sections/` unless stated otherwise.

| Member | Main files |
|---|---|
| Nathan Naylin | `abstract.tex`, `introduction.tex`, `related_work.tex`, `methodology.tex`, `method_systems_nathan.tex`, `method_diagnostics_nathan.tex`, `results.tex`, `results_diagnostics_nathan.tex`, discussion in `discussion_nathan.tex`; coordinates `../main.tex` and `../references.bib` |
| Arizona Xing | `method_data_arizona.tex`, `method_diagnostics_arizona.tex`, `results_diagnostics_arizona.tex` |
| Patricia Jennesha | `method_evaluation_patricia.tex`, `results_quality_patricia.tex`, limitations in `discussion_nathan.tex`, `conclusion_nathan.tex` (Conclusion and Future Work) |
| Zhitong Li | `method_statistics_zhitong.tex`, `results_statistics_zhitong.tex` |
| Jidni Mayukh | `method_sensitivity_jidni.tex`, `results_synthesis_jidni.tex`; prepares figures with the evidence owners |
| Every member; Nathan integrates | Their own paragraph in `author_contributions.tex`; focused Related Work and limitation/future-work inputs |

The existing section filenames are retained for stable links and LaTeX inputs;
Patricia owns the limitations and conclusion/future-work sections even where
the filename ends in `_nathan.tex`.

Nathan's and Arizona's marker-diagnostic files form one printed subsection in
Methodology and one in Results. Their separate files retain ownership and
stable cross-reference labels. Results moves from quality to uncertainty and
accent variation, recognition-error associations, marker diagnostics and
sensitivity checks. Preserve this sequence when editing individual files.

`ai_use_statement.tex` is an optional placeholder, commented out in `main.tex`.
Enable it only after confirming actual use and course guidance. It is not a
mandatory section stated in the supplied final-report instructions.

## Editing the report

1. Use verified prose and preserve section labels and existing `\ref{...}`
   links. Contribution statements must describe completed work.
2. Check table values against the named archives, including score aggregation
   and resampling units. Do not replace missing evidence with assumed results.
3. Figure 1 is inline TikZ in `sections/method_systems_nathan.tex`. Rebuild and
   inspect its rendered layout after changes. Avoid figures that duplicate
   existing tables without adding an explanation.
4. Use `\cite{key}` with the shared `references.bib`. Add sources with verified
   metadata and preserve IEEE first-citation order; do not use `\nocite{*}` to
   reach the minimum.
5. Keep preparation evidence paths in member notes/the Markdown plan. Refer to
   the project's results through paper tables/figures and to the code through the
   existing Methodology footnote, not numbered literature entries.
6. The pdfLaTeX setup includes CJK support for live Chinese examples. Check
   those examples after rebuilding; use typed equations rather than screenshots.

Find unresolved draft content from the repository root:

```sh
rg -n 'TODO|\\placeholder\{|\\figureplaceholder\{|\\scoreblank' research_report/latex
```

This also finds macro definitions in `main.tex`; remove unused draft macros at
final cleanup. Search the sources, not only the PDF, for comments that still
describe planned work. Follow the plan's final audit, including visual review.

## Limits that differ from the literature-survey assignment

- Main body: maximum **12 pages**, excluding Contributions and References.
  Title/abstract, tables, figures, discussion and conclusion count in the body.
- Related Work: maximum **one page**. Abstract: **150–200 words in one paragraph**.
- References: **at least nine** actually cited external sources, **one page maximum**.
- Contributions: **one or two sentences per member**, execution and actual writing.
- No appendix. Important experimental details must appear in the main body.

Author Contributions follows Acknowledgments in normal document flow.
References starts on a dedicated page so that all 25 entries fit on one
physical page, as required by the assignment. This is a report-specific layout
choice rather than a general IEEE requirement. `\IEEEtriggeratref{12}` balances
the bibliography columns; recheck that setting if the references change.
The acknowledgments/contributions page uses the balance package, enabled after
Conclusion and disabled before References. This keeps both columns in use and
lets the Conclusion retain its natural heading spacing.
Both sections are excluded from the body limit. The optional AI statement has no explicit page-
limit exemption; if enabled, include its space in the body allowance. Do not
reduce IEEE margins/fonts to meet the limits. Nathan maintains the planned
11-page body budget and integrates one coherent narrative.
