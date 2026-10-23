# Jidni draft integration review

Integrated on 24 October 2026 from `member_5/jidni_part.md`.
The original Markdown is unchanged.

## Integration

- Replaced the method and results placeholders in
  `latex/sections/method_sensitivity_jidni.tex` and
  `latex/sections/results_synthesis_jidni.tex` with all supplied paragraphs
  and the five-row sensitivity table.
- Converted paragraph labels to IEEE subsubsections, mathematical notation to
  LaTeX, and hard-coded section/table numbers to automatic references.
  The sensitivity table currently resolves to Table VII.
- Added Chinese font support for the supplied example and credited Jidni's
  completed final-report writing in Author Contributions.
- Preserved the submitted wording at integration. A subsequent requested edit
  changed first-person phrases to impersonal academic wording without changing
  their meaning. The interpretation statements below remain unchanged; two
  labels were added to Zhitong's results for cross-references.

## Verification

The subset counts, marker-free intervals, corpus scores, fallback scores,
one-clip-per-speaker intervals and worst-clip summaries agree with the saved
evaluation/synthesis tables. The English/Chinese example appears in
`runs/synthesis_results/worst_clips_by_accent_system.csv`.

The WER-subset intervals are not stored in the existing synthesis CSVs. A
separate CPU-only check on the frozen metric table, using the documented
accent-stratified speaker bootstrap (1,000 resamples, seed 760), reproduced
all WER-subset intervals reported in the draft. The same check reproduced the
saved full-set intervals. No notebook or model inference was run, and no
archived result file was changed.

## Interpretation statements for author review

These statements remain unchanged in the integrated report.

1. **Larger MT:** "A comparison that varies MT capacity alone cannot show what
   a larger or differently trained MT model would do."
   This is unclear because the experiment already compares a larger 3.3B MT
   checkpoint with a smaller 600M checkpoint. It can report their observed
   difference, while conclusions about other model sizes or training regimes
   require further experiments. Clarify whether that narrower limitation was
   intended.
2. **Worst clips:** "A low automatic score on such a clip measures reference
   matching and identifies no system error."
   This may be read as establishing that the translation has no error. A low
   reference-overlap score alone establishes neither an error nor the absence
   of one. The saved zero score and example strings are verified; a human
   judgment that the literal rendering is correct is not established by those
   records.
