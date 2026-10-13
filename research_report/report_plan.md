# Group 9 final research report plan

Prepared on 13 October 2026. This is a writing plan, not the final report.
The assignment contract is [instructions.md](instructions.md). Work allocation
comes from the **named** [README contributions](../README.md#team-member-contributions),
because proposal and literature-survey member numbering differ.

## 1. Report contract

| Requirement | How we will meet it |
|---|---|
| Standard scientific paper | Title, five authors, abstract, introduction, related work, methodology, experiments and results, discussion/limitations, conclusion/future work, contributions, references |
| IEEE two-column format | Reuse the structure and supplied IEEEtran class from `literature_review/latex`; write in `research_report/latex` |
| Body length | Maximum **12 pages excluding Contributions and References**; aim for about **11 pages** including title, abstract, tables and figures |
| Abstract | One paragraph, 150–200 words; Nathan writes it after the results are integrated |
| Introduction | About 1–1.5 pages; explicit research question, testable hypotheses, approach and actual contributions |
| Related Work | **No more than one page**; rewrite a focused synthesis rather than copying the survey |
| Methodology | Enough information to reproduce the experiment from the paper itself, including important data, model, decoding, metric and statistical choices |
| Conclusion | About one page including high-level answers, limitations and realistic master's-project directions |
| Contributions | One or two sentences **per member** covering actual execution and report writing; all members confirm their own statement |
| References | At least nine external references, IEEE style, **maximum one page** |
| Appendix | **None**; essential details must fit in the main paper |
| Code link | Refer to the GitHub implementation in Methodology and give its URL in a footnote |
| Submission | One PDF, `9_FinalReport.pdf`; group leader uploads it by **25 October 2026, 23:59**, using the course deadline |

The Methodology and Results sections are the main body of this empirical
benchmark. We compare existing pretrained systems rather than propose or train
a new algorithm. Give more space to experimental design, uncertainty and
interpretation than to general model background. The rubric puts 33 marks on
Methodology, 44 on Experiments and Results, and 33 on Conclusion/Future Work.

## 2. Project analysis and evidence to use

The implemented project contains data preparation, feasibility pilots, three
full inference runs, three-system scoring, statistical analysis, results
synthesis and two stages of Direct `<unk>` investigation. The final paper
should follow this evidence chain, rather than the older five-accent,
3,000-clip proposal or notebook narratives describing work that was then future.

This planning review inspected the README/run guides, notebook source and saved
outputs, full-run configuration/environment/summary JSONs, evaluation and
statistical CSVs, synthesis tables and supplementary diagnostic records. It
checked counts and sentence-score summaries in the archived evaluation table.
It did **not** execute notebooks, rerun inference, or establish a fresh replay.

| Component | Current project evidence | What it contributes to the paper |
|---|---|---|
| Data preparation — Arizona | `01_data_preprocessing.ipynb`, `02_audio_extraction.ipynb`; frozen metadata is local/Git-ignored | Common Voice Scripted Speech 26.0 English, CoVoST 2 Chinese references matched by normalized English sentence; filtering, speaker cap, sampling and label limitations |
| Pilots and inference — Nathan | Pilot/timing notebooks, `03_direct_pipeline.ipynb`, `04_cascaded_pipeline.ipynb`, merger/archiving helpers; three full-run directories | Frozen model systems, engineering feasibility, preprocessing, deterministic inference, checkpointing, run validation and hardware |
| Quality evaluation — Patricia | `08_evaluation.ipynb`, `runs/evaluation_results/merged_3system_with_metrics.csv`, saved evaluation PDF | Overall and per-accent corpus scores, sentence chrF++, WER and marker flags |
| Statistics — Zhitong | `09_statistical_analysis.ipynb`; `intervals_long.csv`, `accent_means_ci.csv`, `spearman.csv`, `tests.csv` | Paired uncertainty, accent spread and gap variation, association tests and effect sizes |
| Synthesis and sensitivity — Jidni | `10_synthesis_q1_q9.ipynb`; `runs/synthesis_results/` tables, six figures and dashboard | Q1–Q9 synthesis, common marker-free subset, WER subsets, worst clips, fallback and one-clip-per-speaker checks |
| Earlier marker diagnosis — Nathan | Notebooks 05–07; `runs/direct_unk_diagnostic_1789953533/`, `direct_unk_sensitivity_1789954497/`, `direct_literal_unk_blocking_1789970452/`; investigation log | Literal-marker audit, tokenizer checks and 35-clip decoding/constraint experiments |
| Further marker diagnosis — Arizona | Four `unk_analysis/notebooks/`, four scripts and `unk_analysis/results/`; supplementary README | Text-only comparison, 700-clip hidden-token check, generation probabilities, word removal, accent/word-frequency associations |
| Related literature — all, integrated by Nathan | `literature_review/latex/sections/`, shared survey bibliography and individual reading notes | Focused motivation and context; external methods/data citations, not evidence for our own results |

### Frozen experiment facts

- **4,200 clips, seven groups, 600 clips per group**, 1,586 pseudonymous speakers;
  speakers and sentence/reference content repeat. The dataset is balanced by
  clip count, not by independent speakers, sentences or recording conditions.
- Accent groups: England English, Filipino, Hong Kong English, India and South
  Asia (India, Pakistan, Sri Lanka), Malaysian English, Southern African
  (South Africa, Zimbabwe, Namibia), and United States English.
- `sample_id` identifies a repeating pseudonymous **speaker**. The generated
  unique `id` aligns clips across runs; matching row order and dataset hashes
  are necessary. Do not call the data fully anonymous or expose original IDs.
- Direct: `facebook/seamless-m4t-v2-large`, speech to Chinese text (`cmn`).
  Cascades: `openai/whisper-large-v2` English transcription followed by either
  `facebook/nllb-200-distilled-600M` or `facebook/nllb-200-3.3B`
  (`eng_Latn` → `zho_Hans`). Both cascade variants must be reported.
- Same frozen clips/references; mono 16 kHz audio, seed 760, greedy decoding
  (`num_beams=1`, `do_sample=False`, `max_new_tokens=256`). No model training,
  fine-tuning, accent adaptation or manual output correction.
- Each full run has 4,200 successful outputs, zero recorded failures and zero
  generation-limit flags. The two separately run Whisper stages produced
  matching transcript strings for all clips.

### Numerical anchors for drafting

These are saved results, checked against the current tables; they are not new
model runs. Patricia and Zhitong should verify each final table/figure against
the original artifact and retain full precision until display rounding.

| System | Corpus BLEU (`zh`) | Corpus chrF | Corpus chrF++ | Mean sentence chrF++ |
|---|---:|---:|---:|---:|
| Direct | 38.86 | 32.38 | 25.08 | 27.86 |
| Cascade-600M | 29.11 | 24.23 | 18.44 | 20.86 |
| Cascade-3.3B | 31.91 | 26.36 | 20.06 | 22.87 |

| Mean sentence chrF++ comparison | Gap | Speaker-clustered 95% interval |
|---|---:|---:|
| Direct minus Cascade-600M | +7.00 | +6.45 to +7.60 |
| Direct minus Cascade-3.3B | +4.99 | +4.39 to +5.70 |
| Cascade-3.3B minus Cascade-600M | +2.01 | +1.61 to +2.42 |

The main statistical configuration is paired, accent-stratified speaker
resampling, 1,000 bootstrap samples, seed 760 and 95% percentile intervals.
Speaker resampling retains clips together; point estimates remain weighted by
clip counts. Speaker-mean rank tests have a different unit of analysis.

Important interpretation boundaries:

1. Direct leads on the frozen set and its within-accent paired intervals are
   positive. **Higher quality does not establish stronger accent robustness.**
   Intervals for differences in the max-minus-min accent spread include zero.
2. Speaker-level gap variation across accents is detected for Direct versus
   600M (`p=0.0015`) and versus 3.3B (`p=0.0087`), with small reported effects.
   The 3.3B-versus-600M lift has no detected accent variation (`p=0.1682`);
   this does not prove equal lift across accents.
3. Corpus normalized Whisper WER is about 5.97%; mean per-clip WER is 6.32%.
   WER is an ASR diagnostic, not a translation-quality score for Direct.
   WER–cascade sentence chrF++ correlations are weak and negative
   (`rho=-0.188` and `-0.196`), not causal evidence.
4. Direct has **508/4,200** outputs with literal `<unk>` (12.10%; 599
   occurrences). Special UNK IDs and the visible literal string are different
   measurements. The earlier 35-clip sample and later 700-clip sample must
   retain their own denominators and selection rules.
5. Jidni's common marker-free subset contains 3,692 clips. Removing the same
   affected clips from all systems is a sensitivity analysis; it does not
   estimate the causal effect of deleting `<unk>` from an output.
6. The saved fallback check slightly lowers corpus scores (BLEU 38.86 → 38.54;
   chrF++ 25.08 → 24.89). Treat it as a post-hoc check, not an improved deployed
   method. The one-clip-per-speaker check retains positive overall gaps.
7. The supplementary text-only run records 528 affected outputs among 4,200;
   the 700-clip speech check records 74 clips with hidden special UNK IDs.
   Arizona should select a few directly reproducible findings, not reproduce
   every supplementary claim. Some write-up statistics have no supplied
   replication code; the exact mechanism remains unresolved.

## 3. Research argument and questions

Working title: **Regional English Accent Robustness in Direct and Cascaded
Speech-to-Text Translation: An Empirical Study**.

Keep the adopted main question:

> How does regional English accent affect the translation quality of Direct
> and Cascaded speech-to-text translation systems?

Explain that the experiment measures observed system/accent associations on a
frozen English-to-Simplified-Chinese set. Operationalize robustness as variation
in mean sentence chrF++ across the seven groups (including max-minus-min spread),
while reporting overall quality separately.

Group the notebook's Q1–Q9 into three readable report themes. These are a writing
organization, not replacement research questions or nine separate paper sections.

| Report theme | Notebook evidence | Answer the reader needs |
|---|---|---|
| System quality and accent variation | Q1–Q4 | Overall ranking, ranking within accents, between-accent variation, and whether system gaps vary by accent |
| ASR and Direct-output diagnostics | Q5–Q6, selected Q8 | Associations with WER and literal markers, subset results, and a small number of inspected error examples |
| Larger MT model and sensitivity | Q7, Q9 | Whether the 3.3B cascade raises quality or changes accent patterns; whether conclusions survive subset and speaker checks; realistic next steps |

Nathan should state testable comparisons in the Introduction. The following are
**proposed final-report formulations**, not evidence that these exact hypotheses
were registered before results were seen. Check proposal/meeting records before
calling any hypothesis pre-specified.

- **System comparison:** paired mean sentence chrF++ gaps differ from zero;
  report direction and intervals for all three comparisons.
- **Accent variation:** accent-level quality and paired gaps vary, and the
  systems may differ in their between-accent spread. Keep the two claims distinct.
- **ASR association:** higher normalized WER is associated with lower cascade
  sentence chrF++ and wider Direct–Cascade gaps.
- **MT variant comparison:** the 3.3B cascade improves mean sentence chrF++
  over 600M; whether that improvement varies by accent is a separate test.

Marker, fallback, word-removal and subset analyses are explicitly post-hoc and
exploratory. A failed or inconclusive robustness hypothesis is a valid research
result and should remain visible in the conclusion.

## 4. Section plan, owners and space

Page allocations include figures/tables and are targets for the completed
paper, not the current placeholder PDF. Target total: **11 pages** of main body.

| Part | Target | Main writer | Content and LaTeX file(s) |
|---|---:|---|---|
| Title, authors, abstract | 0.50 page | Nathan; all verify | Clear scope and verified headline findings; `main.tex`, `sections/abstract.tex` |
| I. Introduction | 1.25 pages | Nathan | Motivation, main RQ, operational robustness, honest hypotheses, compact approach and actual project contributions; `introduction.tex` |
| II. Related Work | **1.00 page max** | Nathan integrates all members' focused inputs | Three short themes: accent ASR, Direct/Cascaded comparisons/error propagation, and evaluation/data design; finish with how this benchmark fits; `related_work.tex` |
| III-A. Data and references | 0.75 page | Arizona | Provenance/version, accent labels, sentence matching and first-reference policy, normalization, duration/plausibility filters, speaker cap/sampling, speaker/content counts, de-identification; `method_data_arizona.tex` |
| III-B. Systems and execution | 0.75 page | Nathan | Three models, exact resolved revisions, language codes, shared controls, two-pass cascade, alignment/hashes, T4/FP16 environment, timing boundaries; `method_systems_nathan.tex` |
| III-C. Evaluation | 0.50 page | Patricia | Corpus BLEU/chrF/chrF++, sentence chrF++, WER normalization and aggregation, signatures, marker definition; `method_evaluation_patricia.tex` |
| III-D. Statistical analysis | 0.50 page | Zhitong | Estimands and typed gap/spread equations, paired stratified speaker bootstrap, clip sensitivity, rank tests/effects, Dunn–Holm correction scope, correlations; `method_statistics_zhitong.tex` |
| III-E–G. Diagnostic/sensitivity design | 0.50 page total | Nathan, Arizona, Jidni | Each writes their own design briefly: earlier decoding tests, further marker tests, common subsets/speaker/fallback/worst-clip checks; three member-specific method files |
| IV-A. Overall and per-accent quality | 1.00 page | Patricia | Overall score table and concise per-accent evidence; interpret corpus/sentence results and WER; `results_quality_patricia.tex` |
| IV-B. Uncertainty and accent variation | 0.90 page | Zhitong | Paired intervals, accent means/spreads, gap tests/effects and WER associations; explicitly separate quality from robustness; `results_statistics_zhitong.tex` |
| IV-C–D. Marker findings | 1.00 page total | Nathan (about 0.35), Arizona (about 0.65) | Earlier frozen-run/constraint findings; selected text/speech/word-removal findings and unresolved mechanism; two member-specific results files |
| IV-E. Sensitivity and synthesis | 0.60 page | Jidni | Marker-free intervals, WER subsets, 3.3B lift, speaker check, fallback and selected worst-clip interpretation; `results_synthesis_jidni.tex` |
| V. Discussion and limitations | 0.75 page | Nathan integrates members' limitations | Answer RQ across results, quality versus robustness, confounding, dependence, automatic metrics, exploratory tests, diagnostic limits and reproducibility/access; `discussion_nathan.tex` |
| VI. Conclusion and future work | About 1.00 page | Nathan integrates all members | High-level supported answers and prioritized future studies; no new results; `conclusion_nathan.tex` |
| Author Contributions | Excluded | Each member; Nathan integrates | Exactly five confirmed 1–2 sentence statements; `author_contributions.tex` |
| References | Excluded; **1 page max** | All cite; Nathan audits | Shared `references.bib`, IEEEtran BibTeX; at least nine sources actually used |

All section files above are under `latex/sections/`. The Methodology and Results
heading files only open those sections; member files supply their subsections.
This avoids five independent reports and lets members edit their own parts.

## 5. What each member delivers

### Nathan Naylin — organizer, pipelines and earlier diagnostics

Write the title/abstract, Introduction, systems/execution subsection, earlier
diagnostic method/results, integrated Discussion and Conclusion. Integrate the
one-page Related Work from the team's existing reading. Maintain `main.tex`,
shared notation, references, page budget and final PDF. Preserve both cascade
variants and distinguish actual run times from pilot estimates. Nathan also
coordinates handoffs, cross-checks claims, confirms contributions and performs
the final submission checks. These organizer tasks are assigned to Nathan as
requested; they do not replace his technical contribution.

Inputs: Nathan's notebooks and run directories in Section 2, investigation log,
all members' verified section drafts and survey dataset/reference notes.

### Arizona Xing — dataset and further Direct diagnostics

Write `method_data_arizona.tex`, `method_diagnostics_arizona.tex` and
`results_diagnostics_arizona.tex`. Supply the compact dataset table, the exact
reference-matching/filtering/sampling policy, and the important speaker/content
limitations. Select a small reproducible subset of the supplementary marker
findings, retaining sample sizes and visible/hidden-token distinctions.
Contribute Direct/Cascade comparison context from the survey to Related Work.

Inputs: notebooks 01–02, frozen de-identified dataset summaries,
`unk_analysis/README.md`, its notebooks/scripts, JSON summaries and result CSVs.

### Patricia Jennesha — metrics and quality evaluation

Write `method_evaluation_patricia.tex` and `results_quality_patricia.tex`.
Supply the overall score table, per-accent corpus evidence and WER summary.
Record precise metric settings/signatures; explain why corpus scores, sentence
means and WER aggregations differ. Contribute a brief error-propagation/robustness
literature input and automatic-evaluation limitations. Coordinate with Zhitong
on the shared metric table rather than duplicate statistical conclusions.

Inputs: notebook 08, archived evaluation CSV/PDF, evaluation running guide.

### Zhitong Li — statistical method and inferential results

Write `method_statistics_zhitong.tex` and `results_statistics_zhitong.tex`.
Supply the paired-gap interval table and verified annotations for confidence-
interval/accent figures. Report effect sizes, test units and correction scope.
Explain both detected gap variation and inconclusive spread differences.
Supply WER associations and speaker/content-dependence limitations. Contribute
the focused accent-ASR context already reviewed for the survey.

Inputs: notebook 09 and all four statistical CSVs; coordinate input/schema
checks with Patricia and sensitivity intervals with Jidni.

### Jidni Mayukh — synthesis, sensitivity and figures

Write `method_sensitivity_jidni.tex` and `results_synthesis_jidni.tex`.
Select and prepare paper-sized figures from notebook 10 and check their captions,
metric units and source tables with the relevant owner. Cover the common marker-
free subset, zero/positive-WER comparison, larger-MT interpretation, one-clip-
per-speaker and fallback checks. Select at most a few worst-clip examples that
the team can assess accurately; low automatic scores alone are not a verified
linguistic error taxonomy. Provide the cross-result answer matrix and future-work
input to Nathan, using Q1–Q9 as an evidence checklist. Contribute metric/statistical
literature context from the survey.

Inputs: notebook 10, synthesis README/tables/six figures/dashboard, Patricia's
scores, Zhitong's intervals/tests and both members' marker investigations.

Each member also supplies their actual contribution statement, external citation
keys, claim-to-artifact notes, limitations and any borrowed-code/figure credits.
The allocation follows documented work rather than forcing equal word counts.

## 6. Tables, figures and reproducibility details

| Item | Owner(s) | Source / content | Priority |
|---|---|---|---|
| Dataset table | Arizona | Seven groups; clips, speakers, durations and repeated content, from frozen data summaries | Essential |
| System/configuration table | Nathan | Model IDs/revisions, language direction, decoding and execution controls | Essential |
| Architecture diagram | Nathan; Arizona reviews | Adapt the survey's group-created diagram to show **both** NLLB variants and common references; distinguish original drawing from cited model descriptions | Essential |
| Overall quality table | Patricia | Three systems, corpus BLEU/chrF/chrF++, mean sentence chrF++; WER separately labelled | Essential |
| Gap/variation display | Zhitong; Jidni prepares | `intervals_long.csv`, `accent_means_ci.csv`; `q2_per_accent_gaps.png`, `q3_accent_means.png` or a compact combined layout | Essential |
| Diagnostic/subset table | Nathan, Arizona, Jidni | Samples/conditions and literal/special tokens; selected subset intervals and checks | Essential but compact |
| WER or MT-lift figure | Jidni; Patricia/Zhitong verify | `q6_wer_and_spearman.png` or `q7_scale_lift.png` | Include only if it adds information beyond tables |
| Selected translation examples | Jidni; diagnostic owners verify | `worst_clips_by_accent_system.csv`, original predictions/references | Optional; handle Chinese fonts explicitly and verify interpretation |

Avoid including all six dashboard figures. Prefer three or four clear figures
and compact tables; remove duplication before shrinking fonts. Regenerate figures
for two-column print when labels are too small. Do not rely on a dashboard, code
link or appendix for information essential to understand the paper.

The paper must state data provenance/version; accent selection; normalization
and first-match policy; duration/plausibility criteria; seed and speaker cap;
model IDs and resolved revisions; audio/decoding controls; environment; alignment;
metric settings/versions; statistical unit, estimand and resampling settings.
Full hashes may live in the run records if their purpose and validation are
explained. Do not claim new inference is reproducible from a public clone alone:
audio/frozen metadata are not committed. Archived predictions permit CPU scoring
and analysis, subject to documented notebook configuration changes.

## 7. Literature and citation plan

Use the survey as the starting point for **sources and synthesis**, not reusable
pages of final-report prose. Nathan integrates three short Related Work themes:
accent-related ASR evidence (Zhitong), system comparisons/error propagation
(Arizona/Patricia), and matched datasets/evaluation (Nathan/Jidni). Identify how
the completed experiment differs from the cited settings without claiming an
exhaustive or first-ever research gap.

The frame's independent bibliography seeds 13 relevant external entries: Common
Voice, CoVoST 2, accent codebooks, Direct/Cascade context and comparison, Seamless
(the v2 context), Whisper, NLLB, BLEU, chrF, chrF++, SacreBLEU reporting and paired
significance testing. Eleven are copied from the survey bibliography; Whisper and
NLLB metadata were checked against their primary publication pages:
[Whisper](https://proceedings.mlr.press/v202/radford23a.html) and
[NLLB](https://arxiv.org/abs/2207.04672). This metadata check does not replace
reading the papers before making literature claims. Existing survey metadata is
reused, not newly reverified in full.

Use `\cite{key}` where a source supports a claim; do not manually number
references or cite our own result files as literature. Cite our tables/figures
in the paper and keep local evidence paths in preparation notes. Reference the
project repository through the Methodology footnote. Add further sources only
when needed, keeping at least nine actually cited entries and the final list
within one page. Placeholder citations in the frame are reminders and must be
attached to real supported claims during drafting.

## 8. Integration workflow and checks

Suggested internal schedule; Nathan can adjust these team handoff dates:

| Date (October 2026) | Handoff |
|---|---|
| 13–14 | All members read the plan, verify their evidence and confirm current contributions/hypothesis history |
| 15–18 | Member-owned method/results drafts, tables, captions and claim-to-artifact notes delivered |
| 19–20 | Nathan integrates narrative and Related Work; Jidni prepares final-sized figures with owners |
| 21–22 | Cross-review RQ answers, statistics, citations and reproducibility; shorten to the page budget |
| 23–24 | Nathan writes final abstract/conclusion, confirms contributions/AI disclosure and checks the compiled PDF |
| 25 | Final group review and leader submission before 23:59 |

For every handoff, provide the LaTeX file, figure/table source, exact evidence
path, numeric precision/settings, citation keys and any unresolved claim. Use
one naming convention: Direct, Cascade-600M and Cascade-3.3B. Define abbreviations
once. Report score differences in points; distinguish WER percentages from
proportions. Jidni coordinates plots, while each producing member validates the
underlying numbers and remains credited for that work.

Before final submission Nathan checks:

- All required sections exist, every hypothesis/RQ receives a supported answer,
  and interpretations follow the results. No planned experiment appears as done.
- Dataset/model/configuration statements agree across prose, tables and captions.
  Clip IDs and speaker IDs are never confused.
- Corpus and mean sentence scores are labelled correctly. Uncertainty names its
  resampling unit, comparisons keep the same sign, and tests include effects and
  correction scope. Nonsignificance is not equivalence.
- Marker findings retain original/subset denominators and analysis paths. No
  suppressed-marker output is substituted into the frozen benchmark.
- Repeated speakers/content, unmatched accent content, model/training confounds,
  single-reference metrics, post-hoc analyses and access/replay limits are discussed.
- Related Work fits one page; main body fits 12; References fit one page and
  contain at least nine cited external sources; no appendix.
- Five contribution paragraphs describe completed work and actual report
  writing, not merely this proposed assignment. Check any optional AI statement
  against actual use and applicable course guidance.
- GitHub footnote works; all equations are typeset; borrowed/adapted materials
  have credits; no undefined citations/references, overflow or visible TODOs.
- Compile with IEEEtran, inspect every final PDF page, and name the submission
  `9_FinalReport.pdf`. A compiled placeholder frame is not a completed report.

## 9. LaTeX handoff

Entry point: [latex/main.tex](latex/main.tex). Build and editing instructions:
[latex/README.md](latex/README.md). The frame contains member-labelled TODOs,
empty table/figure slots, a Methodology GitHub footnote and a shared IEEE
bibliography. It deliberately leaves the report prose for members to write.

Before drafting, useful known cleanup points are notebook 09's `scip` install
typo and nonexistent standalone-script wording; notebook 08's mutable input URLs
and older narrative; the legacy merger's 600M selection; and supplementary
statistics missing replication code. Use current guides/archived artifacts to
write accurately. Resolving these code issues is separate from this report-frame
task, and none should be silently described as already fixed.
