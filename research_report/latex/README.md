# Group 9 IEEE final-report frame

This is a **placeholder frame**, not a completed report. Read
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

This produces `main.pdf`, currently a draft containing visible TODOs and empty
tables/figures. Its page count does not predict the completed report's length.
Generated PDFs and auxiliary files are ignored by Git.

After every placeholder is replaced and the team has checked the final paper:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=9_FinalReport main.tex
```

This produces the required `9_FinalReport.pdf`. Do not submit the frame preview.
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
Patricia owns the limitations and conclusion/future-work placeholders even where
the filename ends in `_nathan.tex`.

`ai_use_statement.tex` is an optional placeholder, commented out in `main.tex`.
Enable it only after confirming actual use and course guidance. It is not a
mandatory section stated in the supplied final-report instructions.

## Filling the frame

1. Replace your `\placeholder{owner}{instructions}` calls with verified prose.
   Preserve section labels and use the existing `\ref{...}` labels for tables
   and figures. Do not turn a writing assignment into an already-completed
   contribution claim.
2. Fill blank table cells with results from the named archive. Check the score
   aggregation and resampling unit in every caption. Empty dashes are deliberate
   placeholders, not zero measurements.
3. Put final figures in `figures/`. Replace `\figureplaceholder{...}` with, for
   example, `\includegraphics[width=\columnwidth]{figures/accent_gaps.pdf}`.
   The macro itself lives in `main.tex`; remove its definition after all calls
   are gone. Delete optional figure slots that duplicate the text/tables.
4. Use `\cite{key}` with the shared `references.bib`. Its 13 initial entries are
   a focused seed set, not a requirement to cite irrelevant papers. The visible
   citations in TODOs must become supported citations in real prose. Add needed
   sources with verified metadata; do not use `\nocite{*}` to reach the minimum.
5. Keep preparation evidence paths in member notes/the Markdown plan. Refer to
   our own results through paper tables/figures and to the code through the
   existing Methodology footnote, not numbered literature entries.
6. The default pdfLaTeX setup handles the English report. If including Chinese
   translation examples as live text, choose and validate an appropriate CJK
   font/package configuration first; do not paste unsupported Unicode into
   this frame or use screenshots for equations.

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

`\clearpage` separates the body, Contributions and References so their page
boundaries are easy to inspect. The optional AI statement has no explicit page-
limit exemption; if enabled, include its space in the body allowance. Do not
reduce IEEE margins/fonts to meet the limits. Nathan maintains the planned
11-page body budget and integrates one coherent narrative.
