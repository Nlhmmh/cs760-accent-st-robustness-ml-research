# Final research report rubric review

Reviewed on **25 October 2026** against the [assignment instructions and rubric](instructions.md).

Reviewed report: [the latest submission PDF](latex/9_FinalReport.pdf).

Owners below follow the report's section assignments.

The report is strong in experimental documentation, paired evidence and
qualified discussion. The highest-priority remaining work is to correct two
Results interpretations, then complete the WER table label.
The indicative estimate remains **198/220 (90%)**; it is not an official
mark or a prediction of the teaching team's judgment.

## Areas needing improvement

| ID | Priority | Owner | Area | Location | Required improvement |
|---|---|---|---|---|---|
| R1 | High | **Jidni** | Meaning of a zero automatic score | IV-E5, page 10 | Remove the implication that zero reference overlap establishes the absence of a translation error |
| R2 | High | **Jidni** | Incorrect accent-gap ranking | IV-E2, page 9 | The United States group does not have the smallest Direct-minus-Cascade-600M gap; correct or remove that comparison |
| R4 | Medium | **Patricia** | WER aggregation label | Table V, page 7 | Identify the values as mean per-clip normalized WER |

### R1: Zero-score interpretation

**Owner:** Jidni.

**Location:** [Synthesis results](latex/sections/results_synthesis_jidni.tex),
source line 87, Section IV-E5.

The sentence “A low automatic score on such a clip measures reference matching
and identifies no system error” is too strong. The example shows a zero
reference-overlap score; it does not establish whether the translation is
semantically acceptable. A literal rendering of an idiom may itself be wrong.

Suggested replacement:

> A low automatic score on such a clip does not, by itself, establish a
> translation error; qualitative assessment is needed to distinguish reference
> mismatch from an inadequate translation.

This changes the interpretation, not the recorded score.

### R2: Incorrect United States gap ranking

**Owner:** Jidni.

**Location:** [Synthesis results](latex/sections/results_synthesis_jidni.tex),
source lines 62–67, Section IV-E2.

The WER-subset paragraph describes the United States and Malaysian groups as
having “the smallest and one of the largest Direct-minus-Cascade-600M gaps.”

The first part is incorrect. Recomputing accent means from the
[saved evaluation table](../runs/evaluation_results/merged_3system_with_metrics.csv)
gives the following mean sentence chrF++ gaps:

| Accent group | Direct minus Cascade-600M |
|---|---:|
| England | **5.41** |
| Southern African | **5.52** |
| United States | **6.57** |
| Malaysian | **7.86** |

England has the smallest gap. The United States group does have the lowest
share of positive-WER clips, which may be the source of the confusion.
The stated positive-WER shares, **22.8%** for United States and **36.2%**
for Malaysian English, agree with the saved data.

Keep those percentages, but remove the incorrect gap-ranking clause. For example:

> Clips with positive normalized WER account for 22.8% of United States
> English and 36.2% of Malaysian English.

Retain the following caution that the WER split is defined by a system output
and does not isolate a causal accent effect.

### R4: WER aggregation label

**Owner:** Patricia.

**Location:** [Quality Results](latex/sections/results_quality_patricia.tex),
source lines 34–41, Table V.

The prose now identifies mean per-clip normalized WER, but the caption and column still say normalized Whisper WER and WER (%).
The **4.29–8.36%** values are group averages of clip-level normalized WER.

Use **Mean per-clip normalized WER (%)** in the caption or column heading,
and identify that aggregation when discussing the range. It differs from the
overall pooled corpus WER of **5.97%**; the overall mean per-clip WER is
**6.32%**. The saved evaluation table reproduces the per-accent means.

The values themselves do not need to change.

## Indicative rubric marks

**198.00 / 220 = 90.00%.**

Reassessed against the current 12-page PDF using the published rubric bands.
This is an indicative assessment, not an official grade. R1, R2 and R4 remain
open; improvements to formatting and wording do not resolve those findings.

| Criterion | Estimated marks | Current assessment |
|---|---:|---|
| Overall Structure | **11 / 11** | All required sections are present. Methodology and Results receive the greatest emphasis, appropriate for an empirical evaluation. The shorter conclusion still contains synthesis, practical implications, limitations and future work. |
| Abstract and Title | **22 / 22** | The title identifies the accent setting and system comparison. The one-paragraph abstract states motivation, dataset, systems, paired evaluation, numerical findings and unresolved robustness. Its 179 whitespace-separated words (190 TeXcount words) fit the 150–200-word guidance. |
| Introducing the idea: Problem statement | **22 / 22** | The introduction states the research question and testable comparisons, explains their importance, defines robustness separately from average quality and makes the observational scope explicit. |
| Previous Work | **11 / 11** | Five focused themes connect the relevant literature to the experiment. The discussion explains differences in adaptation, language direction, architecture, data and evaluation. Related Work fits entirely on page 2. |
| Methodology | **33 / 33** | Data matching and sampling, exact checkpoints, inference controls, scorer settings, statistical units, speaker-clustered resampling and selected diagnostic samples are described. The metric explanation is now clearer. Missing inference/replay records and possible training overlap are acknowledged as limitations. |
| Experiments and Results | **29.33 / 44** | The report interprets quality rankings, intervals, effect sizes, accent variation, WER associations and sensitivity checks. Two material interpretation errors remain: the zero-score example does not establish semantic correctness (R1), and the United States group is incorrectly called the smallest Direct-minus-Cascade-600M gap (R2). These prevent a confident top-band assessment despite the extensive evidence. |
| Conclusion and Future Work | **33 / 33** | The conclusion answers the main question with the correct scope: Direct leads on this benchmark, while relative accent robustness is unresolved. It adds practical cautions and six future directions linked to limitations. The corrected spread comparison is specific to Direct's lead over the cascades. Its shortness is a soft balance issue rather than a maximum-length violation. |
| Body: Flow of the report | **11 / 11** | The argument progresses from motivation and design through quality, uncertainty, accent variation, ASR associations, diagnostics and sensitivity checks to interpretation. Transitions and the restored IEEE heading hierarchy connect the sections. The final Conclusion text, Acknowledgments and Contributions share page 11 without an unnecessary extra page. |
| Clarity of writing and writing technique | **14.67 / 22** | The prose is generally clear and impersonal, and the IEEE heading/reference formatting is consistent. The zero-score wording remains semantically misleading (R1), and Table V still omits its WER aggregation from the caption/header (R4). Dense technical passages and repetitive limitation-to-study phrasing also leave room for a more concise final edit. |
| Citations / References | **11 / 11** | All 25 bibliography entries are cited, keys resolve and numbering follows first use. The complete reference list fits on page 12 in balanced IEEE columns. Source links and the previously incomplete Card et al. metadata are present. |
| **Total** | **198.00 / 220** | **90.00%** |

The remaining deductions are concentrated in Results interpretation and writing
precision. No deduction is applied merely because Conclusion spans parts of
two physical pages, because the supplied one-page conclusion guidance is
approximate rather than a maximum.

## Current word counts

The assignment specifies **no overall word limit**. It specifies an abstract
length and page limits.

These are TeXcount **text-word** counts. They exclude title/headings,
captions, bibliography entries, table cells and mathematical expressions
according to TeXcount's parsing rules. Technical strings and hyphenated terms
can be counted differently by other tools.

| Section | TeXcount text words |
|---|---:|
| Abstract, excluding index terms | **190** |
| Introduction | **700** |
| Related Work | **423** |
| Methodology, including all member subsections | **2,893** |
| Experiments and Results, including all member subsections | **2,207** |
| Discussion and Limitations | **532** |
| Conclusion and Future Work | **334** |
| Acknowledgments | **65** |
| **Body text total, including Abstract and Acknowledgments** | **7,344** |
| Author Contributions, excluded from the body above | **270** |
| Index terms | **14 words in five terms** |
| **All section text, including Contributions and index terms, excluding References** | **7,628** |

Adding the title/headings (**201 words**) and captions/other counted
non-body text (**263 words**) gives **8,092 words**, still excluding
References, table cells and mathematical expressions.

The abstract has **179 whitespace-separated words** and **190 TeXcount
words**, excluding index terms. Both satisfy the approximate **150–200-word**
requirement. It is one paragraph.

## Current page-limit assessment

The current submission PDF and preview have matching text and contain
**12 physical pages**. The assignment permits **up to 12 body pages, excluding
Contributions and References**. Under a conservative count of every physical
page touched by body content, this report uses **11 body pages**.

| Item | Verified current extent | Requirement | Assessment |
|---|---|---|---|
| Complete PDF | **12 pages** | No separate whole-PDF maximum; the limit applies to the body | **Pass** |
| Main content, including title, abstract and Acknowledgments | Pages **1–11**; page 11 also contains excluded Contributions | At most **12 body pages** | **Pass**; one physical body-page allowance remains |
| Abstract | Page **1**; one paragraph, **179 whitespace-separated / 190 TeXcount words** | About **150–200 words**, one paragraph | **Pass** |
| Introduction | Pages **1–2**, approximately one page of two-column content | About **1–1.5 pages** | **Pass** as an approximate target |
| Related Work | Entirely on page **2** | Maximum **one page** | **Pass**, including a strict physical-page interpretation |
| Methodology | Pages **3–6** | Sufficient detail and emphasis for an empirical evaluation; no separate page maximum | Appropriate emphasis |
| Experiments and Results | Pages **7–10**, including the inference-runtime discussion on page 10; its table appears with Systems and Controlled Inference on page 4 | Results supported by statistics and interpretation; no separate page maximum | Appropriate extent; R1 and R2 remain substantive issues |
| Discussion and Limitations | Page **10** | Limitations may appear in a separate section before Conclusion | **Pass** |
| Conclusion and Future Work | Starts on page **10** and continues on page **11**; **334 text words** | About **one page**, not a one-page maximum | Substantive coverage is present, although the text volume is shorter than the suggested target; spanning two pages is not itself a breach |
| Acknowledgments | Page **11**, after the Conclusion | No separate stated limit or exemption | Included in the 11-page body count |
| Author Contributions | Page **11**, following Acknowledgments and occupying the right column | Excluded from the body limit; **1–2 sentences per member** | **Pass**; five members, two sentences each, covering execution and writing |
| References | All **25 entries on page 12**, in two balanced IEEE columns | At least **nine references**, maximum **one page** | **Pass**, including a strict physical-page interpretation |
| Appendix | None | Not allowed | **Pass** |
| Submission filename | [9_FinalReport.pdf](latex/9_FinalReport.pdf) | Group ID followed by the required suffix | **Pass** |

The final Conclusion text, Acknowledgments and Contributions share page 11.
References occupies page 12 alone. Standard IEEE fonts and margins are
preserved. The dedicated reference page is a layout choice that satisfies
the assignment's one-page reference limit, rather than a general IEEE rule.

There is **no overall word limit** in the supplied instructions. Word-count
figures above are descriptive; they do not create an additional submission
requirement.
