# COMPSCI 760 Literature Survey Plan

## Recommended Literature Survey Strategy

Use a **thematic literature survey**, not a paper-by-paper review.

Recommended structure:

1. **Speech Translation Architectures & System Comparisons**
2. **Accent Robustness in Speech Processing**
3. **Accent Robustness in Speech Translation**
4. **Evaluation Data & Methodological Evidence**

The review should progress from **general → specific**:

**Speech Translation → Direct vs. Cascaded systems → Accent robustness → Accent effects on speech translation → Evaluation evidence → Cross-theme synthesis → Research gap → Research question**

### Paper Target

- 5 group members
- Minimum required: **3 papers per member**
- Recommended total: **about 17 strong papers**
- Maximum allowed: **30 papers**
- Prefer recent peer-reviewed work, while keeping important foundational papers where necessary
- Assign **one primary reader per paper**
- Allow important papers to support more than one theme

---

## Themes and Sub-Themes

| # | Major Theme | Sub-Themes | What to Investigate | Why It Matters to Our RQ | Key Comparisons / Questions | Priority |
|---|---|---|---|---|---|---|
| 1 | **Speech Translation Architectures & System Comparisons** | Direct ST; Cascaded ST; Direct vs. Cascade; ASR→MT error propagation | How Direct and Cascaded systems work; strengths, weaknesses, performance patterns, modularity, and intermediate-error propagation | Our RQ directly compares Direct and Cascaded ST systems | When does Direct/Cascade perform better? Why? What limitations affect robustness comparison? | **Core** |
| 2 | **Accent Robustness in Speech Processing** | Accent effects in ASR; regional/underrepresented English; seen vs. unseen accents; accent adaptation/generalisation | How regional accent affects speech recognition; robustness across accent groups; adaptation approaches and limitations | Establishes why accent is a meaningful variable in speech processing | How large are accent effects? Which accents are affected? How well do systems generalise? | **Core** |
| 3 | **Accent Robustness in Speech Translation** | Accent → translation quality; accented/dialectal ST; Direct vs. Cascade under accent; ASR-error/translation-quality relationship | Whether accent effects carry into final translation and whether Direct and Cascade respond differently | This is the closest literature to the exact research question and should establish or challenge the proposed research gap | Has this already been studied? Are studies measuring ASR only or final translation? Are comparisons controlled? | **Core** |
| 4 | **Evaluation Data & Methodological Evidence** | Accent/ST datasets; reference quality; WER/BLEU/chrF++; balanced evaluation; paired comparison; bootstrap/CI; association analysis | How previous work designs datasets, evaluates quality, controls imbalance, and assesses reliability | Supports defensible methodological choices without turning the LR into a methodology report | Which metrics answer which questions? How do studies control speakers/content? How are differences shown to be reliable? | **Important / Supporting** |

### Important Principle

Do **not** assume the proposed research gap is already true.

The literature search must actively test claims such as:

- accent robustness is studied mainly in ASR rather than final speech translation;
- Direct and Cascaded ST have been compared, but not sufficiently under controlled regional-English accent conditions;
- ASR errors may propagate into Cascaded translation;
- existing experimental settings may make accent-level system comparisons difficult.

If strong existing research already addresses part of the gap, refine the contribution instead of ignoring it.

---

## How the Themes Connect

### Logical Flow

**Theme 1 — Speech Translation Architectures & System Comparisons**  
↓  
Establishes Direct and Cascaded ST, their advantages, limitations, and possible error propagation.

**Theme 2 — Accent Robustness in Speech Processing**  
↓  
Establishes that regional/accent variation can affect ASR and speech processing.

**Theme 3 — Accent Robustness in Speech Translation**  
↓  
Connects the first two themes and investigates whether accent affects final translation differently across Direct and Cascaded systems.

**Theme 4 — Evaluation Data & Methodological Evidence**  
↓  
Examines how previous studies measure these effects and what methodological limitations affect interpretation.

**Cross-Theme Synthesis**  
↓  
**Validated Research Gap**  
↓  
**Research Question**

> **How does regional English accent affect the translation quality of Direct and Cascaded speech-to-text translation systems?**

The final report should read as **one connected argument**, not four independent mini-reviews.

---

## Recommended Search Directions

| Theme / Sub-theme | Search Focus | Example Search Terms | Evidence We Need |
|---|---|---|---|
| Direct vs. Cascaded ST | Architecture comparisons | `"direct speech translation" AND cascaded`; `"cascade versus direct speech translation"`; `"end-to-end speech translation" AND cascade` | Performance patterns, advantages, limitations, experimental conditions |
| ASR→MT error propagation | Intermediate errors affecting translation | `"ASR error propagation" AND "speech translation"`; `"speech recognition errors" AND machine translation`; `"cascade speech translation" AND errors` | Whether ASR errors reduce final translation quality and under what conditions |
| Accent robustness in ASR | Accent-related recognition differences | `"accented speech recognition" AND English`; `"regional accent" AND ASR`; `"accent robustness" AND speech recognition` | Evidence that recognition performance varies across accents |
| Regional / underrepresented accents | Robustness and generalisation | `"underrepresented accents" AND ASR`; `"regional English accents" AND speech recognition`; `"non-native English" AND ASR` | Which groups are underrepresented and how performance differs |
| Seen vs. unseen accents | Generalisation | `"seen unseen accents" AND ASR`; `"accent generalization" AND speech recognition`; `"accent adaptation" AND ASR` | Generalisation and adaptation trade-offs |
| Accent in speech translation | Closest prior work to our RQ | `"accented speech" AND "speech translation"`; `"accent robustness" AND "speech translation"`; `"regional accent" AND "speech-to-text translation"` | Studies that directly or partially address our RQ |
| Dialect/accent × ST architecture | Direct/Cascade robustness | `"dialectal speech translation" AND direct`; `"accent" AND direct AND cascaded AND "speech translation"` | Evidence that may support or weaken our proposed research gap |
| ASR error vs. translation quality | Error relationship | `"WER" AND "translation quality" AND speech`; `"ASR errors" AND "translation quality"` | Evidence linking ASR quality to downstream translation |
| Accent-labelled datasets | Dataset suitability | `"accented speech dataset" AND English`; `"Common Voice" AND accent`; `"regional accent speech dataset"` | Accent labels, speaker coverage, limitations |
| Speech-translation datasets | Human-reference ST data | `"speech translation dataset" AND English`; `"multilingual speech translation corpus"` | Human references, language coverage, dataset limitations |
| Translation metrics | BLEU / chrF / chrF++ | `"speech translation evaluation" AND BLEU`; `"speech translation" AND chrF`; `"machine translation evaluation" AND character metric` | Strengths, weaknesses, and common usage |
| ASR diagnostics | WER | `"WER" AND accented speech`; `"word error rate" AND accent` | Why WER is appropriate for ASR diagnostic analysis |
| Controlled evaluation | Fair comparisons | `"accent evaluation" AND speaker control`; `"speech recognition" AND balanced evaluation` | Speaker/content/duration controls |
| Statistical reliability | Confidence intervals / bootstrap | `"paired bootstrap" AND machine translation`; `"bootstrap confidence interval" AND BLEU`; `"statistical significance" AND speech translation` | Evidence for reliable comparison and uncertainty estimation |
| Contrary evidence | Challenge the proposed gap | `"accent speech translation" review`; `"dialect speech translation" survey`; `"accent robustness" speech translation` | Papers that may already address part of the proposed gap |

---

## How the Five Members Should Divide the Work

### Recommended Division: Hybrid Approach

Do **not** use a strict **one member = one theme** rule.

Use whole-theme ownership for major core themes, while splitting the supporting evaluation/methodology theme.

| Member | Role / Contribution Level | Assigned Theme(s) / Sub-theme(s) | Main Tasks | Approx. Paper Responsibility | Integration Responsibility |
|---|---|---|---|---:|---|
| **Member 1** | **Organizer / Lead Author — smaller LR portion** | Theme 4: **Datasets, reference quality, dataset-design literature** | Read dataset literature; maintain shared tracker/matrix; coordinate structure | **3 papers** | **High:** structure, terminology, transitions, duplicate removal, Introduction→Gap→Conclusion integration, final rubric/format audit |
| **Member 2** | **Main Contributor — ~1/3 of thematic LR work** | **Theme 2: Accent Robustness in Speech Processing** | Accent-ASR evidence; regional accents; seen/unseen accents; adaptation/generalisation; strengths/limitations | **5 papers** | Medium: ensure Theme 2 links clearly into Theme 3 |
| **Member 3** | **Core Contributor** | **Theme 1: Speech Translation Architectures & System Comparisons** | Direct ST; Cascaded ST; Direct-vs-Cascade comparisons; architecture/system strengths and weaknesses | **3 papers** | Medium: coordinate error-propagation boundary with Member 4 |
| **Member 4** | **Core Contributor** | **Theme 3: Accent Robustness in Speech Translation** | Search literature closest to RQ; accent→translation; Direct/Cascade under accent; error propagation | **3 papers** | **High for gap validation:** actively test whether our proposed gap is valid |
| **Member 5** | **Methodological Contributor** | Theme 4: **Metrics, controlled evaluation & statistical evidence** | WER/BLEU/chrF++; paired evaluation; bootstrap/CI; association analysis | **3 papers** | Medium: keep methodology concise and relevant to the research question |

### Why This Allocation Works

- **Member 1** has a smaller literature-writing portion because lead-author integration is substantial work.
- **Member 2** receives the largest substantive theme and approximately one-third of the literature-review workload.
- **Members 3–5** divide the remaining substantive work.
- Every member still personally reads at least **3 papers**.
- Important papers can support multiple themes even when only one member is the primary reader.

---

## Workload Balance Check

| Member | Approx. Share of Thematic LR Work | Additional Responsibilities | Is the Workload Reasonable? |
|---|---:|---|---|
| **Member 1** | **10–12%** | Lead author, integration, terminology consistency, final audit | **Yes** — smaller LR share is offset by major integration work |
| **Member 2** | **32–34%** | Main accent-literature synthesis | **Yes** — intentionally the largest substantive contributor |
| **Member 3** | **19–20%** | Architecture synthesis | **Yes** |
| **Member 4** | **19–20%** | Closest-gap literature + gap validation | **Yes** |
| **Member 5** | **16–18%** | Evaluation/statistical literature | **Yes** |

### Workload Principle

Do not judge workload only by:

- number of themes;
- number of sub-themes;
- number of papers.

Also consider:

- breadth of literature;
- amount of comparison required;
- writing/synthesis complexity;
- integration responsibilities.

---

## Suggested Report Structure and Space Allocation

The final literature survey should follow the required research-paper structure and stay within the **10-page maximum IEEE double-column format**.

| Report Section | Approx. Space | Main Purpose | Primary Responsibility |
|---|---:|---|---|
| **Title + Authors** | Template space | Clearly define the survey scope | Group / Member 1 |
| **Abstract** | ~150–200 words | Motivation, survey scope, main synthesis, gap | Member 1 after body is complete |
| **I. Introduction** | **~1–1.25 pages** | Problem, motivation, RQ, survey scope and organisation | Member 1 + Group |
| **II. Speech Translation Architectures & System Comparisons** | **~1.4 pages** | Direct/Cascade approaches, comparisons, strengths/limitations | Member 3 |
| **III. Accent Robustness in Speech Processing** | **~1.7 pages** | Accent-ASR evidence, regional variation, generalisation, limitations | **Member 2** |
| **IV. Accent Robustness in Speech Translation** | **~1.4 pages** | Intersection of accent + final ST + Direct/Cascade | Member 4 |
| **V. Evaluation Data & Methodological Evidence** | **~1.0 page** | Datasets, reference quality, metrics, controls, statistical evidence | Members 1 + 5 |
| **VI. Cross-Theme Synthesis & Research Gap** | **~0.6–0.8 page** | Combine themes, identify limitations, validate/refine the gap | Member 1 + Member 4 + Group |
| **VII. Conclusion** | **~0.5 page** | Main findings, defensible gap, final RQ | Member 1 + Group |
| **Author Contribution + AI Use Statement** | Short | Transparency | Member 1 |
| **References** | Remaining space | Complete IEEE references | All verify; Member 1 standardises |

### Space Principle

Core themes should receive more space than supporting methodological material.

Do **not** give equal space to all themes just because they have equal labels.

---

## How This Plan Targets Full Marks

| Rubric Criterion | Full-Mark Requirement | How This Plan Addresses It | What We Must Do Well |
|---|---|---|---|
| **Overall Structure — 6 pts** | Title, Authors, Abstract, Introduction, Body, Conclusion, References | All required components are explicitly planned | Do not omit required sections |
| **Abstract & Title — 12 pts** | Clearly describe motivation, methodology/scope, findings and content | Abstract is written after synthesis so it reflects the actual survey | Avoid a generic abstract written before the literature is understood |
| **Problem Statement — 18 pts** | Clearly introduce topic and direction | Introduction moves from ST → accent robustness → system comparison → RQ | Explain why the problem matters, not only what the systems are |
| **Body Flow — 18 pts** | General ideas → specific conclusions; transitions connect sections | Themes are intentionally ordered to create a logical research story | End each section with synthesis and a transition to the next |
| **Completeness — 18 pts** | Good overview; approaches clearly organised; similarities/differences and advantages/disadvantages highlighted | Shared matrix and theme structure force cross-paper comparison | Compare findings and experimental conditions instead of listing papers |
| **Clarity — 18 pts** | Crisp, clear, succinct writing | Lead author standardises terminology, notation, tone and removes repetition | Avoid five disconnected writing styles |
| **Conclusion / RQ — 18 pts** | Precise synthesis; insights and RQ strongly supported by review | Dedicated cross-theme synthesis validates the gap before the conclusion | Every final gap/RQ claim must be supported by evidence from the body |
| **Citations / References — 12 pts** | Complete citations, matching references, consistent IEEE format | One shared evidence matrix + final citation audit | Personally verify every source, claim, number and reference |

### What Full-Mark-Level Work Actually Requires

Having the correct section titles is **not enough**.

For example:

**Weak approach**

> Paper A used Direct ST. Paper B used Cascaded ST. Paper C reported accent errors.

**Stronger synthesis**

> Studies using Direct and Cascaded ST report different performance patterns under different datasets, language pairs, and adaptation settings. The group should compare why findings differ, what each design controls, and whether those results can actually support conclusions about accent robustness.

For every major theme, aim to identify:

- areas of agreement;
- contradictory findings;
- differences in experimental settings;
- strengths;
- weaknesses;
- limitations;
- missing evidence;
- direct relevance to the research question.

The survey should ultimately establish a **defensible research gap from verified evidence**, rather than simply repeating the gap proposed earlier.
