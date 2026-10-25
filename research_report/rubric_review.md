# Final research report rubric review

Reviewed on **25 October 2026** against the [assignment instructions and rubric](instructions.md).

Reviewed report: [the latest submission PDF](latex/9_FinalReport.pdf).

Owners below follow the report's section assignments.

The full report is strong in experimental documentation, paired evidence and
qualified discussion. No material numerical mismatch or unsupported main
conclusion was identified in this review. The remaining suggestions concern
writing precision and sentence density.
The indicative estimate is **212.67/220 (96.67%)**; it is not an official
mark or a prediction of the teaching team's judgment.

The review covered all 22 included section files, all 12 rendered pages,
Tables I–IX, both figures and the reference list. Dataset counts, benchmark
means, saved statistical intervals/tests, diagnostic counts, sensitivity
results and runtime totals were compared with archived CSV/JSON evidence.
Key Related Work claims were also checked against primary publications.
This is an archive-based review, not a fresh model-inference or statistical
replay, and it does not establish translation acceptability by human judgment.

## Areas needing improvement

These are optional final writing improvements rather than unresolved factual
errors or submission-limit breaches.

| Priority | Owner | Area | Location | Suggested improvement |
|---|---|---|---|---|
| Low | **Jidni** | Scope of qualitative assessment | IV-F5, page 10; [source line 88](latex/sections/results_synthesis_jidni.tex#L88) | Clarify that the idiom example was not qualitatively assessed; the report separately describes a 20-pair reference spot-check |
| Low | **Zhitong and Jidni; Nathan integrates** | Sentence density | III-D, IV-B and IV-F5 | Split the long bootstrap-method sentence and selected diagnostic sentences, retaining the sampling units, numerical evidence and uncertainty qualifications |

For the qualitative-assessment suggestion, the current example correctly distinguishes reference
mismatch from translation correctness. If the intended scope is this particular
example, an optional clearer ending is: “This example was not qualitatively
assessed.” This avoids suggesting that no qualitative reference checking was
performed anywhere in the study.

## Indicative rubric marks

**212.67 / 220 = 96.67%.**

Reassessed against the current 12-page PDF using the published rubric bands.
This is an indicative assessment, not an official grade. The remaining
deduction concerns writing density and precision.

| Criterion | Estimated marks | Current assessment |
|---|---:|---|
| Overall Structure | **11 / 11** | All required sections are present. Methodology and Results receive the greatest emphasis, appropriate for an empirical evaluation. The shorter conclusion still contains synthesis, practical implications, limitations and future work. |
| Abstract and Title | **22 / 22** | The title identifies the accent setting and system comparison. The one-paragraph abstract states motivation, dataset, systems, paired evaluation, numerical findings and unresolved robustness. Its 192 whitespace-separated words (195 TeXcount words) fit the 150–200-word guidance. |
| Introducing the idea: Problem statement | **22 / 22** | The introduction states the research question and four labelled hypotheses, explains their importance, defines robustness separately from average quality and makes the observational scope explicit. |
| Previous Work | **11 / 11** | Five focused themes connect the relevant literature to the experiment. The discussion explains differences in adaptation, language direction, architecture, data and evaluation. Related Work fits entirely on page 2. |
| Methodology | **33 / 33** | Data matching and sampling, exact checkpoints, inference controls, scorer settings, statistical units, speaker-clustered resampling and selected diagnostic samples are described. The notation and two typed equations are consistent with the analysis. Full-run environment records and metadata fingerprints support the benchmark comparison. Missing versions for some later diagnostic runs, incomplete replay records and possible training overlap are acknowledged limitations. |
| Experiments and Results | **44 / 44** | The report interprets quality rankings, intervals, effect sizes, accent variation, WER associations and sensitivity checks. The positive-WER shares and the three-lowest/four-highest group comparison agree with the saved 4,200-row evaluation table. The zero-score example now separates reference mismatch from translation acceptability. H1–H4, Figure 2 and the Discussion connect the evidence to the research question while retaining observational and uncertainty limits. |
| Conclusion and Future Work | **33 / 33** | The conclusion answers the main question with the correct scope: Direct leads on this benchmark, while relative accent robustness is unresolved. It adds practical cautions and six future directions linked to limitations. It distinguishes observed accent means from statistically detected differences. Its shortness is a soft balance issue rather than a maximum-length violation. |
| Body: Flow of the report | **11 / 11** | The argument progresses from motivation and design through quality, uncertainty, accent variation, ASR associations, diagnostics, runtime and sensitivity checks to interpretation. Results and Discussion link H1–H4 to their evidence and retain the distinction between higher quality and stronger accent robustness. Figure 2 shows accent means and intervals. The sensitivity section leads directly into Discussion. Conclusion, Acknowledgments and Contributions share page 11 without an unnecessary extra page. |
| Clarity of writing and writing technique | **14.67 / 22** | The prose is generally clear and impersonal, with no first-person wording found in the included sections. IEEE headings, equations and label-based references are consistent. Selected statistical and diagnostic sentences remain dense, and the qualitative-assessment scope could be clearer. These issues keep the writing below the rubric's crisp, clear and succinct top band. |
| Citations / References | **11 / 11** | All 25 numbered references were checked against primary publication, dataset or software records. Author attribution, titles, years, venues, applicable volume/issue/page fields and DOI/URL targets agree with those records. All are cited, keys resolve and numbering follows first use. IEEEtran formats author lists consistently, and the complete list fits on page 12. No unresolved metadata or reference-format error was identified. |
| **Total** | **212.67 / 220** | **96.67%** |

The remaining deduction concerns writing density and precision. The Conclusion
is shorter than the suggested one-page target, which is approximate rather
than a maximum. It still answers the research question and gives six future
directions linked to limitations.

## Reference check

The check covered all **25 numbered references**, including conference and
journal papers, arXiv preprints, the Common Voice release metadata and the
wordfreq and spaCy software citations. The [shared bibliography](latex/references.bib)
contains the primary-source links. Original publication years were checked
separately from later revision or online-digitisation dates; page ranges and
volume/issue numbers were checked where applicable. A DOI is not invented for
records whose primary publication page does not provide one.

Author lists follow the [IEEE Reference Guide](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf):
up to six names are displayed, and longer lists use the lead author followed
by “et al.” The bibliography-format control is not a numbered reference.
The Kruskal–Wallis and Dunn entries use their canonical publisher DOI links:
[Kruskal and Wallis](https://doi.org/10.1080/01621459.1952.10483441) and
[Dunn](https://doi.org/10.1080/00401706.1964.10490181).
The repeated-author dash in the chrF++ entry is normal IEEEtran formatting.
The spaCy year and DOI agree with the [maintainers' preferred citation](https://github.com/explosion/spaCy/blob/master/CITATION.cff).

Both PDFs retain the same 25 references in first-citation order. The rendered
reference page has no clipping, overlaps or overflow; standard IEEE fonts and
margins are preserved.

## Current word counts

The assignment specifies **no overall word limit**. It specifies an abstract
length and page limits.

These are TeXcount **text-word** counts. They exclude title/headings,
captions, bibliography entries, table cells and mathematical expressions
according to TeXcount's parsing rules. Technical strings and hyphenated terms
can be counted differently by other tools.

| Section | TeXcount text words |
|---|---:|
| Abstract, excluding index terms | **195** |
| Introduction | **647** |
| Related Work | **423** |
| Methodology, including all member subsections | **2,872** |
| Experiments and Results, including all member subsections | **2,220** |
| Discussion and Limitations | **545** |
| Conclusion and Future Work | **332** |
| Acknowledgments | **65** |
| **Body text total, including Abstract and Acknowledgments** | **7,299** |
| Author Contributions, excluded from the body above | **270** |
| Index terms | **14 words in five terms** |
| **All section text, including Contributions and index terms, excluding References** | **7,583** |

Adding the title/headings (**199 words**) and captions/other counted
non-body text (**281 words**) gives **8,063 words**, still excluding
References, table cells and mathematical expressions.

The abstract has **192 whitespace-separated words** and **195 TeXcount
words**, excluding index terms. Both satisfy the approximate **150–200-word**
requirement. It is one paragraph. TeXcount does not count the `\unk{}` helper;
counting the displayed marker as one word gives **196 words**.

## Current page-limit assessment

The current submission PDF and preview have matching text and contain
**12 physical pages**. The assignment permits **up to 12 body pages, excluding
Contributions and References**. Under a conservative count of every physical
page touched by body content, this report uses **11 body pages**.

| Item | Verified current extent | Requirement | Assessment |
|---|---|---|---|
| Complete PDF | **12 pages** | No separate whole-PDF maximum; the limit applies to the body | **Pass** |
| Main content, including title, abstract and Acknowledgments | Pages **1–11**; page 11 also contains excluded Contributions | At most **12 body pages** | **Pass**; one physical body-page allowance remains |
| Abstract | Page **1**; one paragraph, **192 whitespace-separated / 195 TeXcount words** | About **150–200 words**, one paragraph | **Pass** |
| Introduction | Pages **1–2**, approximately one page of two-column content | About **1–1.5 pages** | **Pass** as an approximate target |
| Related Work | Entirely on page **2** | Maximum **one page** | **Pass**, including a strict physical-page interpretation |
| Methodology | Pages **3–6** | Sufficient detail and emphasis for an empirical evaluation; no separate page maximum | Appropriate emphasis |
| Experiments and Results | Pages **6–10**, including Figure 2 on page 8 and the inference-runtime discussion on page 9; its table appears with Systems and Controlled Inference on page 4 | Results supported by statistics and interpretation; no separate page maximum | Appropriate extent; the checked Results interpretations agree with the saved evidence |
| Discussion and Limitations | Pages **10–11** | Limitations may appear in a separate section before Conclusion | **Pass** |
| Conclusion and Future Work | Page **11**; **332 text words** | About **one page**, not a one-page maximum | Substantive coverage is present, although the text volume is shorter than the suggested target |
| Acknowledgments | Page **11**, after the Conclusion | No separate stated limit or exemption | Included in the 11-page body count |
| Author Contributions | Page **11**, following Acknowledgments and occupying the right column | Excluded from the body limit; **1–2 sentences per member** | **Pass**; five members, two sentences each, covering execution and writing |
| References | All **25 entries on page 12**, in two balanced IEEE columns | At least **nine references**, maximum **one page** | **Pass**, including a strict physical-page interpretation |
| Appendix | None | Not allowed | **Pass** |
| Submission filename | [9_FinalReport.pdf](latex/9_FinalReport.pdf) | Group ID followed by the required suffix | **Pass** |

All 12 pages were visually inspected. Tables, diagrams, plot labels, equations
and the Chinese example are legible, with no visible clipping or overlaps.
The preview and submission builds report no overflow, undefined-reference,
missing-character or column-balancing warnings.

The final Conclusion text, Acknowledgments and Contributions share page 11.
References occupies page 12 alone. Standard IEEE fonts and margins are
preserved. The dedicated reference page is a layout choice that satisfies
the assignment's one-page reference limit, rather than a general IEEE rule.

There is **no overall word limit** in the supplied instructions. Word-count
figures above are descriptive; they do not create an additional submission
requirement.
