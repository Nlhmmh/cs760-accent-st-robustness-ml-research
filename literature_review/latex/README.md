# COMPSCI 760 literature survey LaTeX project

This directory is a compile-ready IEEE two-column scaffold. `.latexmkrc`
resolves `IEEEtran.cls` from the supplied
`../IEEE-conference-template-062824/` directory. It contains the
complete group-report structure. Member 1's organizational and dataset-review
work and Member 2's supplied accent-ASR review are integrated; placeholders
remain where no member-authored literature prose was supplied.

## Build

From this directory:

```sh
latexmk -pdf main.tex
```

Clean generated build files without deleting the PDF:

```sh
latexmk -c main.tex
```

When verified citations have been added to `references.bib`, change
`\hasverifiedreferencesfalse` to `\hasverifiedreferencestrue` in `main.tex`.
Then run `latexmk -pdf main.tex` again.

The full-width dataset comparison table is kept hidden while it has no
verified rows. After adding at least one evidence-checked row in
`sections/evaluation.tex`, change `\showdatasettablefalse` to
`\showdatasettabletrue` in that file.

## Ownership and planned space

| File / section | Owner | Final space |
|---|---|---:|
| `sections/abstract.tex` | Member 1 + group, completed last | 150--200 words |
| `sections/introduction.tex` | Member 1 + group | about 1--1.25 pages |
| `sections/architectures.tex` | Member 3 | about 1.4 pages |
| `sections/accent_asr.tex` | Member 2 | about 1.7 pages |
| `sections/accent_st.tex` | Member 4 | about 1.4 pages |
| `sections/evaluation.tex`, subsections A--C | Member 1 | part of about 1 page |
| `sections/evaluation.tex`, subsections D--E | Member 5 | part of about 1 page |
| `sections/synthesis_gap.tex` | Member 1 + Member 4 + group | about 0.6--0.8 page |
| `sections/conclusion.tex` | Member 1 + group | about 0.5 page |
| Contributions, AI statement, references | Member 1 coordinates; all verify | short / remaining space |

The final paper must not exceed 10 IEEE double-column pages. References count
toward the limit unless the course staff explicitly says otherwise.

## Working rules

1. Search for `TODO(` before every review or handoff.
2. Replace only placeholders owned by you unless the relevant owner agrees.
3. Read every cited paper in the original. Do not write from an abstract-only
   view, a search snippet, or an AI-generated summary.
4. Put the evidence for each paper in your own notes before adding prose.
5. Attach a citation to every literature-specific claim, comparison, number,
   dataset property, or limitation.
6. Prefer synthesis across papers: agreement, disagreement, experimental
   differences, strengths, weaknesses, and missing evidence.
7. Do not infer final translation robustness from WER alone.
8. Do not assume the candidate research gap is true. Search for contrary work.
9. Keep terminology and capitalization consistent with the list below.
10. Before submission, remove all visible placeholder boxes and resolve every
    TODO; update the AI Use Statement to match actual use.

## Member 1 evidence checklist

Before replacing the three Member 1 placeholders in `evaluation.tex`, record
evidence from approximately three personally read papers covering:

- accent-labelled English speech data;
- speech-translation data and target references;
- label provenance and granularity;
- speaker and content coverage or imbalance;
- human-reference creation and quality control;
- split, matching, duration, and recording-condition limitations;
- what each design allows the research question to claim;
- complete, verified BibTeX metadata.

Do not turn this part into the project's methodology. Its job is to compare
what the literature's datasets and reference designs make possible.

## Terminology

- **Direct speech translation (Direct ST):** source speech to target text
  without an exposed intermediate transcript.
- **Cascaded speech translation (Cascaded ST):** ASR output followed by MT.
- **ASR:** automatic speech recognition.
- **MT:** machine translation.
- **WER:** word error rate; an ASR diagnostic, not a translation metric.
- **BLEU:** a translation evaluation metric; introduce its exact use from a
  verified source.
- **chrF / chrF++:** translation evaluation metrics; distinguish them and cite
  verified definitions.
- **Accent / dialect:** do not use interchangeably unless a cited source does;
  explain that source's terminology.
- **Robustness, adaptation, generalisation:** define operationally when first
  used and apply consistently.

## Final integration audit

- Required structure: title, authors, abstract, introduction, thematic body,
  conclusion, and references.
- At least three personally read papers per member; no more than 30 overall.
- Citation keys and bibliography entries match in both directions.
- One coherent general-to-specific argument with transitions.
- Claims, numbers, tables, equations, and adapted figures are verified.
- Research-gap claims survive a search for contrary evidence.
- Author Contributions and AI Use Statement describe actual work truthfully.
- The PDF compiles without undefined citations, references, or layout defects.
