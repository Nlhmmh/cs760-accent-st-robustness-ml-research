# Final research report rubric review

Reviewed on **24 October 2026** against the [assignment instructions and rubric](instructions.md).

Reviewed report: [the latest submission PDF](latex/9_FinalReport.pdf).

Owners below follow the report's section assignments.

The report is strong in experimental documentation, paired evidence and
qualified discussion. The highest-priority remaining work is to correct two
Results interpretations, then improve metric explanations and labels.
The indicative estimate remains **198/220 (90%)**; it is not an official
mark or a prediction of the teaching team's judgment.

## Areas needing improvement

| ID | Priority | Owner | Area | Location | Required improvement |
|---|---|---|---|---|---|
| R1 | High | **Jidni** | Meaning of a zero automatic score | IV-E5, page 9 | Remove the implication that zero reference overlap establishes the absence of a translation error |
| R2 | High | **Jidni** | Incorrect accent-gap ranking | IV-E2, page 9 | The United States group does not have the smallest Direct-minus-Cascade-600M gap; correct or remove that comparison |
| R3 | Medium | **Patricia** | BLEU tokenizer and chrF++ explanation | III-C, pages 4–5 | Describe 13a accurately and distinguish observed metric values from a general property of Chinese scoring |
| R4 | Medium | **Patricia** | WER aggregation label | Table IV, page 7 | Identify the values as mean per-clip normalized WER |
| R5 | Medium | **Patricia** | Interpretation of MT model scale | IV-A, pages 6–7 | Attribute the observed difference to the two evaluated checkpoints, without isolating parameter count as the cause |

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

### R3: Metric explanation

**Owner:** Patricia.

**Location:** [Evaluation Metrics](latex/sections/method_evaluation_patricia.tex),
source lines 8–16, Section III-C.

Two explanations need more precise wording:

- The default 13a BLEU tokenizer also applies punctuation-oriented rules; it
  is not simply whitespace splitting. The relevant distinction is that it
  does not perform the Chinese segmentation supplied by the zh tokenizer.
- chrF++ uses its own word extraction rather than BLEU's Chinese tokenizer.
  Lower chrF++ than chrF is observed for these outputs; it should not be
  presented as an inevitable property of Chinese or as a directly comparable
  quality decrease across two different metric definitions.

Suggested wording:

> BLEU uses SacreBLEU's Chinese tokenizer because it segments Chinese
> characters, unlike the default 13a tokenizer. chrF++ uses its own
> whitespace-based word extraction with punctuation handling. In this
> evaluation, chrF++ scores are lower than chrF scores; the two metric
> definitions should not be interpreted as interchangeable quality scales.

The version-pinned primary implementations support these distinctions:
[13a](https://github.com/mjpost/sacrebleu/blob/v2.6.0/sacrebleu/tokenizers/tokenizer_13a.py),
[regular-expression tokenization](https://github.com/mjpost/sacrebleu/blob/v2.6.0/sacrebleu/tokenizers/tokenizer_re.py)
and [chrF](https://github.com/mjpost/sacrebleu/blob/v2.6.0/sacrebleu/metrics/chrf.py).
No scoring-setting change is needed to correct the explanation.

### R4: WER aggregation label

**Owner:** Patricia.

**Location:** [Quality Results](latex/sections/results_quality_patricia.tex),
source lines 34–41, Table IV.

The caption and column currently say normalized Whisper WER and WER (%).
The **4.29–8.36%** values are group averages of clip-level normalized WER.

Use **Mean per-clip normalized WER (%)** in the caption or column heading,
and identify that aggregation when discussing the range. It differs from the
overall pooled corpus WER of **5.97%**; the overall mean per-clip WER is
**6.32%**. The saved evaluation table reproduces the per-accent means.

The values themselves do not need to change.

### R5: MT checkpoint comparison

**Owner:** Patricia.

**Location:** [Quality Results](latex/sections/results_quality_patricia.tex),
source lines 25–27, Section IV-A.

“The difference between them reflects translation-model scale” can imply
that parameter count has been isolated as the cause. The experiment compares
two particular NLLB checkpoints with identical saved ASR transcripts.

Suggested replacement:

> Because the two cascades use identical saved Whisper transcripts, their
> score difference reflects the change between the evaluated NLLB checkpoints
> at the translation stage.

The revised sensitivity and Discussion sections already use this more careful
scope. Match their wording consistently; retain the reported numerical gains.

### Optional finishing improvements

- **Conclusion balance — Patricia:** the conclusion has 275 text words, roughly one-third
  of a two-column page, compared with the suggested one page. It already gives
  synthesis and prioritized future work. Add explanation only if it strengthens
  the practical interpretation or explains why a proposed next study resolves
  an uncertainty; do not add filler.
## Indicative rubric marks

**198.00 / 220 = 90.00%.**

| Criterion | Estimated marks | Current assessment |
|---|---:|---|
| Overall Structure | **11 / 11** | All required sections are present. Methodology and Results receive most of the space, appropriate for an empirical comparison. The conclusion is shorter than the suggested length but includes synthesis, limitations and future directions. |
| Abstract and Title | **22 / 22** | The title identifies the comparison and accent setting. The single-paragraph abstract covers motivation, systems, data, paired evaluation, numerical findings and unresolved robustness, within the required word range. |
| Introducing the idea: Problem statement | **22 / 22** | The research question, motivation, hypotheses and observational scope are explicit. The introduction distinguishes ASR from translation outcomes and defines accent robustness separately from overall quality. |
| Previous Work | **11 / 11** | The focused synthesis connects accent recognition, translation architectures, recognition errors, data and evaluation to this study. Differences from prior work are explained, and the whole section fits on page 2. |
| Methodology | **33 / 33** | Data construction, checkpoints, inference controls, scoring settings, paired statistics, speaker dependence and diagnostic samples are documented. The main analyses can be reproduced from archived predictions; inference and environment limits are acknowledged. Minor metric-explanation issues remain under Clarity. |
| Experiments and Results | **29.33 / 44** | The report presents and interprets rankings, intervals, effect sizes, ASR associations and sensitivity checks. The unsupported zero-score interpretation (R1), incorrect United States gap ranking (R2) and checkpoint-scale wording (R5) prevent a confident top-band assessment. |
| Conclusion and Future Work | **33 / 33** | The conclusion synthesizes the supported ranking and unresolved robustness question. It prioritizes matched speaker/content sampling and human evaluation, with six future directions linked to limitations. Its shortness is treated as a soft balance issue rather than a failed maximum-length requirement. |
| Body: Flow of the report | **11 / 11** | Results progresses from quality to uncertainty and accent variation, ASR associations, marker diagnostics and sensitivity checks. Shared diagnostic headings, transitions and the combined Discussion interpretation connect the analyses. |
| Clarity of writing and writing technique | **14.67 / 22** | Remaining ambiguity concerns the zero-score interpretation, Table IV's WER aggregation label, the tokenizer/chrF++ explanation, checkpoint-scale attribution (R1–R5). |
| Citations / References | **11 / 11** | All 25 references are cited, keys resolve and numbering follows first citation. The complete list fits on page 12 in balanced IEEE columns. Card et al.'s page range and publisher are present; every entry has a rendered source link and arXiv identifiers are consistent. |
| **Total** | **198.00 / 220** | **90.00%** |

## Current word counts

The assignment specifies **no overall word limit**. It specifies an abstract
length and page limits.

These are TeXcount **text-word** counts. They exclude title/headings,
captions, bibliography entries, table cells and mathematical expressions
according to TeXcount's parsing rules. Technical strings and hyphenated terms
can be counted differently by other tools.

| Section | TeXcount text words |
|---|---:|
| Abstract, excluding index terms | **187** |
| Introduction | **700** |
| Related Work | **423** |
| Methodology, including all member subsections | **2,849** |
| Experiments and Results, including all member subsections | **2,079** |
| Discussion and Limitations | **547** |
| Conclusion and Future Work | **275** |
| Acknowledgments | **65** |
| **Body text total, including Abstract and Acknowledgments** | **7,125** |
| Author Contributions, excluded from the body above | **270** |
| Index terms | **14 words in five terms** |
| **All section text, including Contributions and index terms, excluding References** | **7,409** |

Adding the title/headings (**191 words**) and captions/other counted
non-body text (**229 words**) gives **7,829 words**, still excluding
References, table cells and mathematical expressions.

The abstract has **183 whitespace-separated words** and **187 TeXcount
words**, excluding index terms. Both satisfy the approximate **150–200-word**
requirement. It is one paragraph.

## Current page-limit assessment

The submission PDF and preview contain **12 physical pages** and have matching
extracted text. The assignment allows **at most 12 body pages excluding
Contributions and References**; it does not impose a 12-page limit on the
complete PDF.

| Item | Current extent | Requirement | Assessment |
|---|---|---|---|
| Main content, including title, abstract and Acknowledgments | Body touches pages **1–11**; the remainder of page 11 contains excluded Contributions | At most **12 body pages** | **Pass**, even counting all physical pages touched by the body |
| Introduction | Pages **1–2**, approximately one page of two-column content | About **1–1.5 pages** | **Pass** as an approximate target |
| Related Work | Entirely on page **2** | Maximum **one page** | **Pass** |
| Methodology | Pages **3–6** | Sufficient detail and emphasis for an empirical evaluation | Appropriate emphasis; no separate section maximum |
| Experiments and Results | Pages **6–9** | Results and supporting statistics, with interpretation | Appropriate emphasis; see R1, R2 and R5 |
| Discussion and Limitations | Pages **9–10** | Limitations may precede Conclusion in a separate section | **Pass** |
| Conclusion and Future Work | Page **10**, roughly one-third of a two-column page; 275 text words | About **one page** | Shorter than suggested, but substantive synthesis and prioritized future work are present; this is a soft length target |
| Acknowledgments | Page **11**, before Contributions | No separate limit or exemption | Included in the body count |
| Author Contributions | Page **11** | Excluded from the body limit; 1–2 sentences per member | **Pass**; five members and two sentences each, covering execution and writing |
| References | All **25 entries on page 12**, in two balanced columns | At least **nine references**, maximum **one page** | **Pass** |
| Appendix | None | Not allowed | **Pass** |
| Submission filename | [9_FinalReport.pdf](latex/9_FinalReport.pdf) | Group ID followed by the required suffix | **Pass** |

References starts on a dedicated page to satisfy the assignment's one-page
limit. This is a layout choice for this report, not a general IEEE requirement.
The standard IEEE font sizes and margins are retained. Related Work and
References now each occupy only one physical page.
