# SeamlessM4T `<unk>` Investigation Log

**Project:** COMPSCI 760 — Robustness and Accent Sensitivity in Direct vs. Cascaded Speech-to-Text Translation  
**Direct system:** `facebook/seamless-m4t-v2-large`  
**Target language:** Mandarin / Simplified Chinese (`cmn`)  
**Status date:** 21 September 2026  
**Purpose of this document:** Record the full context, observations, hypotheses, diagnostic work, implementation problems, sensitivity experiments, results, failed mitigations, conclusions, and defensible reporting language related to the Direct system's visible `<unk>` output.

---

## 1. Executive Summary

During evaluation of the Direct speech-to-text translation system, SeamlessM4T v2-large produced the literal string `<unk>` in a substantial subset of Chinese translations.

The original frozen Direct run contained:

- **4,200 total clips**
- **508 clips containing literal `<unk>`**
- **12.10% of all Direct outputs affected**
- **599 total literal `<unk>` occurrences**
- no failed inference samples
- no generation-limit flags

The investigation initially considered several possible explanations:

1. the Chinese tokenizer might not contain the required characters;
2. the model might be generating SeamlessM4T's special unknown token;
3. greedy decoding might be causing the issue;
4. accent-related speech recognition difficulty might be causing the issue;
5. longer utterances might be reaching the generation limit;
6. the output-processing code might be introducing `<unk>`;
7. the model itself might have learned `<unk>`-like fallback behaviour.

The experiments ruled out or weakened several of these explanations.

The most important technical finding was that the visible string `<unk>` was **not produced using the tokenizer's special UNK token ID (`1`)**. Instead, the model generated ordinary tokens that literally spell the text:

```text
< + unk + >
```

In the 35-clip sensitivity subset, the two observed sequences were:

```text
[249371, 2105, 248948] -> ['<', 'unk', '>']
[9614,   2105, 248948] -> ['▁<', 'unk', '>']
```

These accounted for **39 visible `<unk>` occurrences** in the baseline sensitivity outputs.

Two mitigation strategies were then tested:

- suppressing the special UNK token ID;
- blocking the ordinary token sequences that spell `<unk>`.

Neither provided a reliable solution.

Suppressing special UNK ID `1` had **no effect at all**, because the model was not generating that ID.

Blocking the literal `<unk>` sequences removed the exact form `<unk>`, but the model circumvented the restriction by producing an alternative form:

```text
<unk >
```

All 35 tested clips still contained this unknown-style marker. The constrained outputs also became substantially worse:

| Condition | BLEU | chrF | chrF++ |
|---|---:|---:|---:|
| Baseline greedy | 28.19 | 24.85 | 18.86 |
| Block exact literal `<unk>` | 15.52 | 19.15 | 14.49 |
| Change | **-12.67** | **-5.70** | **-4.38** |

Therefore, the final conclusion is:

> **Simple decoding constraints do not provide a reliable fix for this SeamlessM4T `<unk>` behaviour. The original frozen model outputs should remain unchanged in the main experiment, and the `<unk>` phenomenon should be reported as an observed Direct-system failure mode.**

The experiments do **not** establish the exact internal neural cause. The evidence is most consistent with a model/decoder-side learned generation behaviour rather than a simple missing-Chinese-character problem, special-UNK-token problem, generation-length problem, or purely accent-specific problem.

---

# 2. Research Project Context

## 2.1 Main research question

The broader COMPSCI 760 project asks:

> **How does regional English accent affect the translation quality of Direct and Cascaded speech-to-text translation systems?**

The comparison is between:

### Direct system

```text
English speech
    ↓
SeamlessM4T v2-large
    ↓
Chinese translation
```

### Cascaded system

```text
English speech
    ↓
Whisper large-v2
    ↓
English ASR transcript
    ↓
NLLB-200 distilled 600M
    ↓
Chinese translation
```

The systems are evaluated as complete systems. This is a **system-level comparison**, not a pure architecture ablation, because the systems use different model families, capacities, training objectives, and internal representations.

---

## 2.2 Evaluation dataset

The final evaluation dataset contains:

- **7 regional English accent groups**
- **600 clips per group**
- **4,200 clips total**
- human Chinese reference translations matched from CoVoST2
- Common Voice English speech/audio
- the same audio/reference pair used when comparing Direct and Cascade for a given sample

Accent groups:

1. England English
2. India and South Asia
3. Malaysian English
4. United States English
5. Southern African
6. Filipino
7. Hong Kong English

The Direct `<unk>` investigation was performed **after the original frozen evaluation outputs had already been generated**.

Therefore, all mitigation experiments are explicitly treated as:

> **post-hoc sensitivity analyses**

and not as replacements for the original experiment.

---

# 3. Original Direct Pipeline

## 3.1 Exact model

```text
Model:
facebook/seamless-m4t-v2-large

Revision:
5f8cc790b19fc3f67a61c105133b20b34e3dcb76

Target:
cmn
```

---

## 3.2 Original decoding configuration

The original Direct run used deterministic greedy decoding:

```python
num_beams = 1
do_sample = False
max_new_tokens = 256
```

There was:

- no fine-tuning;
- no accent-specific adaptation;
- no manual translation correction;
- no post-hoc lexical replacement;
- no model-weight update.

The model was evaluated as a frozen pretrained system.

---

## 3.3 Original compute environment

The original full Direct experiment used:

```text
GPU: Tesla T4
Device: CUDA
Precision: FP16
```

The completed Direct run reported approximately:

- **4,200 / 4,200 successful samples**
- **0 failed samples**
- **0 generation-limit flags**
- total end-to-end runtime: **3898.567 seconds**
- approximately **65.0 minutes**
- mean end-to-end runtime: **0.928 seconds/clip**
- median: **0.878 seconds/clip**
- mean model generation: **0.898 seconds/clip**
- mean real-time factor: **0.220**
- peak allocated GPU memory: **2.876 GB**

This matters for the `<unk>` investigation because it rules out a simple explanation such as:

> "The model produced `<unk>` because output generation hit the 256-token limit."

The original run recorded **zero generation-limit flags**.

---

# 4. Initial `<unk>` Observation

## 4.1 Overall frequency

The first systematic diagnostic found:

```text
Total Direct outputs:        4,200
Outputs containing <unk>:      508
Affected rate:              12.095%
Literal <unk> occurrences:      599
```

So approximately:

> **1 in 8 Direct translations contained at least one literal `<unk>` marker.**

---

## 4.2 Number of `<unk>` occurrences per translation

| Literal `<unk>` count in one output | Number of clips |
|---:|---:|
| 0 | 3,692 |
| 1 | 434 |
| 2 | 60 |
| 3 | 11 |
| 4 | 3 |

Most affected outputs contained exactly one marker, but a smaller number contained multiple markers.

---

# 5. `<unk>` by Accent Group

The diagnostic notebook calculated the following descriptive rates:

| Accent group | Clips | Clips with `<unk>` | Total `<unk>` tokens | Affected rate |
|---|---:|---:|---:|---:|
| England English | 600 | 81 | 99 | 13.50% |
| India and South Asia | 600 | 80 | 99 | 13.33% |
| Malaysian English | 600 | 78 | 94 | 13.00% |
| United States English | 600 | 76 | 83 | 12.67% |
| Southern African | 600 | 66 | 79 | 11.00% |
| Filipino | 600 | 65 | 74 | 10.83% |
| Hong Kong English | 600 | 62 | 71 | 10.33% |

The range is:

```text
10.33% – 13.50%
```

This is not a dramatic concentration in one accent group.

### Interpretation

This weakens the hypothesis that `<unk>` is primarily an accent-specific failure.

However, this does **not** prove that accent has no effect. Accent groups also differ in:

- speakers;
- recording conditions;
- sentence content;
- speaker frequency;
- sentence frequency.

Therefore, the safe statement is:

> **The visible `<unk>` phenomenon was distributed across all seven accent groups and did not appear strongly concentrated in one group.**

Do not state:

> "Accent does not affect `<unk>`."

That would require stronger controlled inference.

---

# 6. Length, Runtime, and Generated-Token Patterns

Affected outputs were descriptively somewhat longer.

| Measure | Contains `<unk>` | No `<unk>` |
|---|---:|---:|
| Mean source words | 9.88 | 8.86 |
| Median source words | 10 | 8 |
| Mean audio duration | 5.05 s | 4.56 s |
| Median audio duration | 4.86 s | 4.34 s |
| Mean Direct runtime | 1.053 s | 0.911 s |
| Mean generation runtime | 1.021 s | 0.881 s |
| Mean generated tokens | 19.37 | 14.33 |
| Median generated tokens | 19 | 14 |
| Maximum generated tokens | 42 | 36 |

### Interpretation

Affected samples tend to have:

- slightly longer source sentences;
- slightly longer audio;
- more generated target tokens.

This may simply provide more opportunities for problematic vocabulary/content to occur.

It does **not** establish that sentence length causes `<unk>`.

Importantly:

```text
maximum observed generated tokens in affected set = 42
generation limit = 256
```

So the `<unk>` issue is not explained by reaching the maximum generation length.

---

# 7. Qualitative Example

One visible example from the original Direct output was:

```text
Sample:
sample_0002

English:
However, after persistent calls, Hall-Jones reluctantly accepted despite having no parliamentary ambitions.

Human Chinese reference:
然而，经过不断的电话，Hall-Jones 还是不情愿地接受了，尽管他在议会里毫无野心。

Direct output:
然而,在持续的呼叫之后,霍尔-<unk>斯不情愿地接受了,尽管没有议会野心.
```

The visible `<unk>` appeared inside the transliteration of the name `Hall-Jones`.

This initially raised the possibility that the tokenizer might not contain the necessary target-side characters.

That hypothesis was investigated later and was not supported for the tested Chinese lexical items.

---

# 8. Repeated-Sentence Analysis

A particularly useful diagnostic was to inspect source sentences that occurred more than once in the evaluation dataset.

There were **301 repeated sentence IDs**.

Their `<unk>` behaviour was:

| Pattern | Repeated sentence IDs |
|---|---:|
| Never produced `<unk>` | 256 |
| Always produced `<unk>` | 43 |
| Mixed behaviour | 2 |

Among repeated sentences that produced `<unk>` at least once:

```text
43 always-UNK
2 mixed
```

Therefore:

```math
43 / (43 + 2) = 95.6%
```

of repeated sentences that were affected at least once were affected in **every observed occurrence**.

Examples of repeated sentences classified as `always_unk` included:

```text
Another reason why Apple is superior to Microsoft, the troll posted and grabbed some popcorn for the subsequent flame war.

You will need some rubber boots.

He stood irresolute for a moment and then scrambled out of the pit.

The diver forced open the oyster, revealing a shimmering pearl.

Take shelter in this tent, but keep still.

The hydrogen gas escaped.
```

### Why this matters

Different recordings of the same sentence may involve:

- different speakers;
- different accents;
- different audio.

Yet the same sentence often showed the same `<unk>` behaviour.

This supports the interpretation that `<unk>` is strongly associated with:

- sentence content;
- lexical content;
- model target-generation behaviour;

rather than being purely driven by one speaker/accent.

### What this does not prove

It does not prove:

- accent is irrelevant;
- content is the sole cause;
- the exact neural mechanism.

A safe statement is:

> **Repeated-sentence consistency suggests that the `<unk>` behaviour is strongly content/model-related rather than purely speaker- or accent-specific.**

---

# 9. Early Hypotheses Considered

During the investigation, the following hypotheses were considered.

## Hypothesis A — Missing Chinese vocabulary

Possible explanation:

> SeamlessM4T cannot represent particular Chinese words or characters, so it outputs `<unk>`.

Examples suspected included concepts such as:

```text
苹果
骆驼
帐篷
旗帜
草莓
疲倦
花生
```

This was tested directly.

**Result:** not supported for these tested words.

---

## Hypothesis B — The model is generating its special UNK token

Possible explanation:

> The generated sequence contains SeamlessM4T's actual `unk_token_id`.

This was also tested directly.

**Result:** not supported in the 35-clip sensitivity sample.

---

## Hypothesis C — Greedy decoding is too restrictive

Possible explanation:

> `num_beams=1` makes the model choose `<unk>` even though an alternative valid sequence exists.

Beam search was tested.

**Result:** beam search helped only slightly and did not solve the problem.

---

## Hypothesis D — Accent recognition difficulty causes `<unk>`

Possible explanation:

> Some accent groups cause the model to be uncertain, resulting in `<unk>`.

Evidence considered:

- accent-level rates;
- repeated-sentence consistency.

**Result:** the phenomenon was not strongly concentrated by accent; sentence/content consistency was stronger.

This does not eliminate accent as a factor, but it weakens the idea that accent is the primary explanation for this particular visible marker.

---

## Hypothesis E — Output reaches the generation cap

Possible explanation:

> The model reaches `max_new_tokens=256`, causing an abnormal fallback.

**Result:** ruled out for the observed run.

No generation-limit flags were recorded, and affected outputs had at most approximately 42 generated tokens.

---

## Hypothesis F — The notebook/output code inserts `<unk>`

The original Direct pipeline:

- calls the processor;
- sends model inputs to the model;
- calls `model.generate(...)`;
- decodes model outputs;
- stores the decoded text.

There was no manual rule inserting `<unk>` into translations.

**Result:** the output-processing code was not manually adding the marker.

---

# 10. External Corroboration

An external search was performed to determine whether similar Chinese `<unk>` output had been reported by other SeamlessM4T users.

## 10.1 Meta Seamless Communication issue

A report in Meta's official `facebookresearch/seamless_communication` repository described frequent `<unk>` output for Mandarin and Cantonese, including examples such as an English interjection being translated with a visible `<unk>` prefix.

Reference:

- Meta GitHub issue #168:  
  <https://github.com/facebookresearch/seamless_communication/issues/168>

This is useful corroboration that visible Chinese `<unk>` output has been observed by other users.

It should **not** be described as proof that the exact root cause in this project is identical.

Use:

> **"Similar Mandarin `<unk>` behaviour has been reported in Meta's official Seamless repository."**

Avoid:

> **"This is a confirmed SeamlessM4T bug with the same cause."**

unless Meta explicitly confirms the same root cause.

---

## 10.2 Meta's official UNK-blocking option

Meta's Seamless inference implementation exposes:

```text
--text_unk_blocking
```

and when enabled it sets:

```python
text_generation_opts.unk_penalty = torch.inf
```

Reference:

- <https://github.com/facebookresearch/seamless_communication/blob/main/src/seamless_communication/cli/m4t/predict/predict.py>

This provided the motivation for testing UNK suppression.

However, the later token-level investigation showed that the visible `<unk>` in this Hugging Face inference path was not actually generated using the special UNK token ID.

That explains why special-token suppression did not solve the observed behaviour.

---

# 11. Diagnostic Notebook

Notebook:

```text
05_direct_unk_diagnostic.ipynb
```

Main goals:

1. measure `<unk>` frequency;
2. compare descriptive rates across accent groups;
3. compare affected and unaffected sample characteristics;
4. examine repeated sentences;
5. inspect tokenizer behaviour;
6. test suspicious Chinese words.

Generated artifacts included:

```text
accent_unk_summary.csv
all_direct_unk_rows.csv
diagnostic_summary.json
manual_tokenizer_tests.csv
repeated_sentence_unk_summary.csv
unk_count_distribution.csv
unk_vs_nonunk_numeric_summary.csv
```

---

# 12. Tokenizer Diagnostic

The exact tokenizer loaded from the Direct model was:

```text
Tokenizer:
SeamlessM4TTokenizerFast

UNK token:
<unk>

UNK token ID:
1
```

---

## 12.1 Manual Chinese vocabulary tests

The following items were encoded by the tokenizer:

| Text | Example tokenizer output | Actual UNK ID present? |
|---|---|---|
| 苹果 | `['▁', '苹果']` | No |
| 骆驼 | `['▁', '骆', '驼', '<pad>']` | No |
| 帐篷 | `['▁', '帐', '篷', '<pad>']` | No |
| 旗帜 | `['▁', '旗', '帜', '<pad>']` | No |
| 草莓 | `['▁', '草', '莓', '<pad>']` | No |
| 疲倦 | `['▁', '疲', '倦', '<pad>']` | No |
| 花生 | `['▁花', '生']` | No |

### Interpretation

The tested Chinese words/characters can be represented without `unk_token_id=1`.

Therefore, the simple explanation:

> "The model outputs `<unk>` because these Chinese characters are missing from the tokenizer vocabulary"

is not supported by these tests.

This does not prove that every possible target string is perfectly covered, but it rules out the obvious lexical examples tested.

---

# 13. Reference-Tokenizer Diagnostic and an Important False Lead

The diagnostic initially reported:

```text
3,498 / 4,200 reference translations tokenized with an UNK ID
```

and among the 508 Direct-affected rows:

```text
448 references tokenized with an UNK ID
```

At first, this appeared to suggest broad target-vocabulary coverage problems.

Closer inspection showed this was misleading.

Within the **508 affected Direct rows**:

```text
Reference rows with tokenizer UNK:                   448
Of those ending in Chinese full stop "。":           447
Reference-tokenizer UNK not ending in "。":            1
```

This strongly indicates that the reference-tokenizer diagnostic was largely reacting to punctuation handling, especially the Chinese full stop, rather than demonstrating that the meaningful Chinese lexical items were unavailable.

### Lesson

Do not use:

> **"3,498 references contain unknown vocabulary."**

That interpretation is unsupported and misleading.

A safer description is:

> **"A reference-tokenizer check produced many UNK IDs, but inspection showed that this diagnostic was largely driven by Chinese punctuation, so it was not used as evidence of lexical vocabulary failure."**

---

# 14. Implementation and Environment Problems Encountered

Several technical problems occurred while building and running the investigation notebooks. These are recorded here because they affected reproducibility and explain later environment choices.

---

## 14.1 Hugging Face 401 / expired OAuth token

An early attempt to load the processor failed with:

```text
401 Client Error: Unauthorized
OAuth token has expired: "exp" claim timestamp check failed
```

The later `RepositoryNotFoundError` message was secondary/misleading.

Resolution:

```bash
hf auth logout
hf auth login
hf auth whoami
```

Then restart the notebook/kernel.

This was an authentication problem, not a model-identifier problem.

---

## 14.2 Missing `protobuf`

After authentication was fixed, loading the tokenizer failed with:

```text
ModuleNotFoundError: No module named 'google'
```

followed by:

```text
ImportError: requires the protobuf library
```

Resolution:

```bash
python -m pip install -U protobuf sentencepiece
```

or in the notebook:

```python
%pip install -U protobuf sentencepiece
```

followed by a kernel restart.

Important:

```text
google.protobuf
```

is provided by the `protobuf` package. Installing a generic package called `google` was not the intended fix.

---

## 14.3 Pandas `crosstab` 2-D error

The diagnostic notebook later failed with:

```text
ValueError:
Data must be 1-dimensional, got ndarray of shape (4200, 2)
```

Cause:

The notebook cell containing:

```python
pred = pd.concat(
    [pred.reset_index(drop=True), reference_info.reset_index(drop=True)],
    axis=1,
)
```

had been rerun, creating duplicate diagnostic column names.

Therefore:

```python
pred["reference_tokenizer_has_unk"]
```

returned two columns rather than a one-dimensional Series.

Resolution:

- remove already-created diagnostic columns before recomputing;
- assign each diagnostic column explicitly rather than repeatedly concatenating;
- check:

```python
assert not pred.columns.duplicated().any()
```

This was a notebook-state/Pandas issue, not a SeamlessM4T issue.

---

## 14.4 Local MP3 decoding problem

The sensitivity notebook initially failed on:

```python
torchaudio.load(...)
```

with:

```text
RuntimeError:
Couldn't find appropriate backend to handle ... .mp3
```

The file existed; the local torchaudio environment lacked an appropriate MP3 decoding backend at that point.

Possible fixes considered:

```bash
brew install ffmpeg
brew install libsndfile
python -m pip install -U soundfile
```

and a `librosa` fallback was added to the notebook.

The final 35-sample sensitivity outputs recorded:

```text
loader_used = torchaudio
```

for all selected clips.

---

## 14.5 Hardware mismatch during sensitivity testing

The original 4,200-sample Direct experiment used:

```text
Tesla T4
CUDA
FP16
```

The small sensitivity experiments were run locally as:

```text
CPU
FP32
PyTorch 2.8.0
Torchaudio 2.8.0
Transformers 4.57.6
SacreBLEU 2.6.0
```

This is an important limitation.

The fresh greedy baseline reproduced the saved original translation exactly for:

```text
94.2857%
```

of the 35 selected samples:

```text
33 / 35
```

The baseline reproduction check was therefore retained in every interpretation.

This means small metric differences in the sensitivity experiment should not be treated as formal main-system results without reproducing them in the original T4/FP16 environment.

---

# 15. Sensitivity Experiment 1 — Special UNK Blocking and Beam Search

Notebook:

```text
06_direct_unk_sensitivity.ipynb
```

## 15.1 Sample

A balanced subset was selected from the 508 originally affected outputs:

```text
5 affected clips per accent group
7 accent groups
35 clips total
```

All selected samples originally contained literal `<unk>`.

---

## 15.2 Conditions

Four decoding conditions were tested:

### A. Baseline greedy

```python
num_beams=1
do_sample=False
max_new_tokens=256
```

### B. Greedy + special UNK suppression

Same settings, plus suppression of:

```text
unk_token_id = 1
```

### C. Beam search

```python
num_beams=5
do_sample=False
max_new_tokens=256
```

### D. Beam search + special UNK suppression

Beam-5 plus suppression of token ID `1`.

---

# 16. Sensitivity Experiment 1 Results

| Condition | n | BLEU | chrF | chrF++ | Outputs with literal `<unk>` |
|---|---:|---:|---:|---:|---:|
| Baseline greedy | 35 | 28.19 | 24.85 | 18.86 | 35 |
| Greedy + block special UNK ID | 35 | 28.19 | 24.85 | 18.86 | 35 |
| Beam-5 | 35 | 29.11 | 25.63 | 19.45 | 34 |
| Beam-5 + block special UNK ID | 35 | 29.11 | 25.63 | 19.45 | 34 |

---

## 16.1 Special UNK blocking did nothing

For every condition:

```text
generated_unk_ids = 0
```

The baseline visibly contained `<unk>`, but token ID `1` never occurred in the generated token IDs.

Therefore:

```python
suppress_tokens=[1]
```

had nothing to suppress.

The following pairs were identical:

```text
baseline_greedy
=
greedy_block_unk
```

and:

```text
beam5
=
beam5_block_unk
```

with respect to output quality and literal `<unk>` frequency.

### Conclusion

> **The visible `<unk>` is not the tokenizer's generated special UNK token.**

This was the key turning point in the investigation.

---

# 17. Beam Search Result

Beam-5 changed some translations and reduced the selected-subset `<unk>` count only slightly:

```text
Greedy: 35 / 35 affected
Beam-5: 34 / 35 affected
```

Metrics on the same 35 clips changed by approximately:

```text
BLEU:   +0.92
chrF:   +0.78
chrF++: +0.58
```

Mean runtime changed from approximately:

```text
Greedy: 2.03 sec/sample
Beam-5: 3.72 sec/sample
```

or approximately **84% slower** in the local CPU sensitivity environment.

### Interpretation

Beam search can occasionally find an alternative translation without `<unk>`, but:

- it did not solve the issue;
- 34 of 35 selected outputs remained affected;
- the experiment was small;
- it was run on CPU/FP32 rather than the original T4/FP16 environment.

Therefore:

> **Greedy decoding alone is not a sufficient explanation for the `<unk>` phenomenon.**

---

# 18. Important Beam-Search Example

A useful example involved the word "tulips".

English:

```text
Restoration silver is characterized by embossed motifs for tulips and naturalistic fruit and leaves.
```

Baseline greedy:

```text
修复银的特点是<unk>花和自然的水果和叶子的雕刻图案.
```

A beam-search variant produced a valid lexical alternative:

```text
郁金香
```

for "tulips" in this example.

This demonstrated that alternative decoding can sometimes avoid the fallback marker.

However, the overall experiment showed that this was the exception rather than a general solution.

---

# 19. Critical Discovery — `<unk>` Was Spelled by Ordinary Tokens

The generated token IDs were inspected directly.

The tokenizer's special UNK token was:

```text
<unk>
```

with:

```text
unk_token_id = 1
```

But the generated sequences contained **zero instances of ID 1**.

Instead, the literal string was built from ordinary tokens.

Two sequences were discovered:

| Token IDs | Token strings | Decoded text | Observed occurrences |
|---|---|---|---:|
| `[249371, 2105, 248948]` | `['<', 'unk', '>']` | `<unk>` | 37 |
| `[9614, 2105, 248948]` | `['▁<', 'unk', '>']` | `<unk>` | 2 |

Total:

```text
37 + 2 = 39
```

literal `<unk>` occurrences in the 35 selected baseline clips.

Conceptually:

```text
What was initially assumed:

special token ID 1
        ↓
      <unk>


What was actually observed:

ordinary token "<"
        +
ordinary token "unk"
        +
ordinary token ">"
        ↓
      <unk>
```

### Consequence

Special-token suppression:

```python
suppress_tokens=[1]
```

cannot prevent a string generated through ordinary tokens.

This explains the complete failure of the first UNK-blocking experiment.

---

# 20. Sensitivity Experiment 2 — Block the Literal Token Sequence

Notebook:

```text
07_direct_literal_unk_blocking_sensitivity.ipynb
```

The next experiment tested a stronger constrained-decoding intervention.

The two observed ordinary-token sequences were forbidden using:

```python
bad_words_ids = [
    [249371, 2105, 248948],
    [9614,   2105, 248948],
]
```

The experiment kept:

```python
num_beams=1
do_sample=False
max_new_tokens=256
```

and changed only the decoding constraint.

This was still **not fine-tuning**.

No model weights were changed.

---

# 21. Why Literal-Sequence Blocking Is Not Fine-Tuning

Fine-tuning would involve:

```text
training examples
    ↓
loss calculation
    ↓
backpropagation
    ↓
weight updates
    ↓
changed model
```

The constrained-decoding experiment instead did:

```text
unchanged pretrained model
    ↓
generate next-token probabilities
    ↓
forbid one particular sequence
    ↓
choose another available sequence
```

Therefore, it should be described as:

> **constrained decoding**

or:

> **post-hoc decoding constraint**

not fine-tuning.

---

# 22. Sensitivity Experiment 2 — Initial Reported Result

The notebook's exact-string checker initially reported:

```text
Baseline literal <unk> outputs: 35 / 35
Blocked literal <unk> outputs:   0 / 35
Translations changed:           35 / 35
```

At first sight, this appeared successful.

However, the detector used:

```python
"<unk>" in translation
```

which only matches the exact character sequence:

```text
<unk>
```

It does not match:

```text
<unk >
```

Closer inspection revealed that the apparent success was false.

---

# 23. What the Model Did After Literal `<unk>` Was Blocked

After the exact `<unk>` token sequences were blocked, all **35 / 35** constrained outputs contained the alternative form:

```text
<unk >
```

A robust check:

```python
r"<\s*unk\s*>"
```

matches all 35 constrained outputs.

So:

```text
exact "<unk>":       0 / 35
UNK-like marker:    35 / 35
```

The model did not learn or discover the correct translation merely because one spelling was forbidden.

It found another permitted route.

---

# 24. Alternative Token Sequences After Blocking

Inspection of the constrained generated token IDs showed new recurring sequences:

```text
[9614,   2105, 6679]
[249371, 2105, 6679]
```

Observed counts in the 35 blocked outputs:

```text
[9614,   2105, 6679] -> 172 occurrences
[249371, 2105, 6679] ->  38 occurrences
```

Total:

```text
210 UNK-like occurrences
```

The decoded outputs showed these as the alternative marker:

```text
<unk >
```

rather than the forbidden exact form:

```text
<unk>
```

This shows that an exact sequence blacklist can be circumvented by a closely related alternative tokenization/output form.

---

# 25. Degenerate Output Caused by Literal Blocking

The most severe example was:

```text
sample_2757

English:
Hey look, a flying pig!

Human reference:
嘿，看，一只飞猪！
```

After exact `<unk>` blocking, the output degenerated into repeated:

```text
<unk > <unk > <unk > <unk > ...
```

This sample contained approximately:

```text
85
```

occurrences of the alternative `<unk >` marker.

This is strong evidence that the decoding constraint can make generation behaviour worse rather than fixing the underlying translation uncertainty.

---

# 26. Examples Before and After Literal Blocking

## Example A — "tulips"

English:

```text
Restoration silver is characterized by embossed motifs for tulips and naturalistic fruit and leaves.
```

Reference:

```text
修复银的特点是压花图案表现的郁金香和自然的水果和树叶。
```

Baseline:

```text
修复银的特点是<unk>花和自然的水果和叶子的雕刻图案.
```

Blocked:

```text
修复银的特点是<unk > 郁金香和自然的水果和叶子的雕刻图案.
```

Interesting detail:

- the valid word `郁金香` appears after blocking;
- but the model still generates the alternative unknown-style marker.

So even a locally improved lexical choice does not mean the mitigation works globally.

---

## Example B — "red skirt"

English:

```text
Who is the blonde girl with the red skirt?
```

Reference:

```text
那个穿红裙子的金发女孩是谁?
```

Baseline:

```text
那个穿着红色<unk>子的金发女孩是谁?
```

Blocked:

```text
那个穿着红色<unk > 裙子的金发女孩是谁?
```

The correct concept `裙子` becomes visible, but `<unk >` still remains.

---

## Example C — lexical behaviour unchanged

English:

```text
They walked in from the rain, all dishevelled and steaming.
```

Baseline:

```text
他们从雨中走进来, 所有的<unk>乱和蒸汽.
```

Blocked:

```text
他们从雨中走进来, 所有的<unk > 乱和蒸汽.
```

The constraint changes the surface form but does not solve the translation.

---

# 27. Literal-Blocking Metric Result

The constrained-decoding experiment caused a major quality decline.

| Metric | Baseline greedy | Block exact literal `<unk>` | Change |
|---|---:|---:|---:|
| BLEU | 28.1866 | 15.5150 | **-12.6716** |
| chrF | 24.8505 | 19.1475 | **-5.7030** |
| chrF++ | 18.8636 | 14.4878 | **-4.3758** |

Mean runtime:

```text
Baseline greedy:           2.0236 sec/sample
Literal-sequence blocked:  3.0023 sec/sample
```

approximately:

```text
+48.4%
```

slower in this local CPU experiment.

### Interpretation

The literal constraint:

- removed one exact character pattern;
- did not remove the model's unknown-style fallback behaviour;
- caused the model to generate a variant `<unk >`;
- sometimes caused severe repetition;
- substantially reduced corpus translation scores.

Therefore:

> **Literal-sequence blocking is not a suitable mitigation for the main experiment.**

---

# 28. Why the Notebook Initially Said "0 `<unk>`"

The second sensitivity notebook defined:

```python
contains_literal_unk = "<unk>" in translation
```

This is an exact substring test.

It correctly answers:

> "Does this exact five-character sequence occur?"

But it does not answer:

> "Does any `<unk>`-like marker occur?"

For future diagnostics, use a normalized regex such as:

```python
import re

bool(
    re.search(
        r"<\s*unk\s*>",
        translation,
        flags=re.IGNORECASE,
    )
)
```

This detects:

```text
<unk>
<unk >
< unk>
< unk >
```

depending on spacing.

### Correct interpretation of experiment 2

Do **not** report:

> "Blocking eliminated UNK in all 35 samples."

Report:

> **"Blocking eliminated the exact `<unk>` spelling, but all 35 samples generated an alternative `<unk >` form, so the underlying behaviour was not resolved."**

---

# 29. What Has Been Ruled Out or Weakened

## 29.1 Simple Chinese character OOV explanation

**Weakened / not supported for tested words.**

The manually tested Chinese terms did not encode to the tokenizer's special UNK ID.

---

## 29.2 Special UNK token generation

**Ruled out for the 35-sample sensitivity set.**

Generated special UNK IDs:

```text
0
```

despite visible `<unk>` output.

---

## 29.3 Generation length limit

**Ruled out as the explanation for the observed run.**

- no generation-limit flags;
- affected outputs far below 256 tokens.

---

## 29.4 Output code manually inserting `<unk>`

**Not supported.**

The model output was decoded directly; no custom replacement inserted `<unk>`.

---

## 29.5 Greedy decoding as the sole cause

**Weakened.**

Beam-5 only reduced the affected count from:

```text
35 -> 34
```

in the selected subset.

---

## 29.6 Accent as the primary cause of the visible marker

**Weakened, but not ruled out as a contributing factor.**

Evidence:

- rates across accent groups were relatively close;
- repeated sentence behaviour was highly consistent across multiple speakers/accents.

---

## 29.7 Exact sequence blocking as a fix

**Rejected.**

The model generated `<unk >` instead and translation metrics deteriorated strongly.

---

# 30. What Is Still Unknown

The investigation does **not** establish the exact internal neural cause.

Open possibilities include:

- learned fallback behaviour inherited from model training data;
- decoder preference for textual `<unk>`-style strings in uncertain lexical contexts;
- interaction between multilingual tokenization and model training conventions;
- alignment/representation uncertainty for some source concepts;
- target-generation calibration issues;
- training-corpus artefacts;
- interactions between speech encoding and target decoding.

These possibilities should be described as hypotheses, not conclusions.

Do not claim:

> "The tokenizer is definitely broken."

Do not claim:

> "The model does not know these Chinese words."

Do not claim:

> "Accent causes the unknown token."

Do not claim:

> "The exact neural mechanism has been identified."

---

# 31. Current Best Technical Interpretation

The most defensible interpretation from the accumulated evidence is:

> **The Direct system exhibits a learned target-generation failure mode in which SeamlessM4T sometimes emits the literal textual marker `<unk>` using ordinary vocabulary tokens. The behaviour is not simply the model's special UNK token, is not explained by the generation cap, and cannot be safely repaired by blocking the visible token sequence.**

A shorter presentation version:

> **SeamlessM4T sometimes spells `<unk>` using normal tokens rather than emitting its special UNK token. Blocking either the special token or the exact spelling did not provide a reliable fix.**

---

# 32. Why This Is a Useful Research Finding

The failed mitigation is still informative.

The experiment established that:

1. the marker is a real model output phenomenon;
2. it affects a non-trivial portion of the Direct evaluation set;
3. it is strongly associated with lower translation quality;
4. it recurs for the same sentence content;
5. it is not simply a special-token decoding event;
6. straightforward decoding suppression can make output worse;
7. post-hoc removal of the marker would not be scientifically justified.

This is therefore a valid qualitative model-failure observation.

The research contribution is **not**:

> "We fixed SeamlessM4T."

It is:

> **"We identified, diagnosed, and stress-tested a systematic Direct-system output failure mode while preserving the integrity of the original frozen benchmark."**

---

# 33. Relationship to Translation Quality

Earlier evaluation showed that outputs containing `<unk>` had substantially lower BLEU than unaffected Direct outputs.

Recorded descriptive comparison:

```text
BLEU with <unk>:     25.64
BLEU without <unk>:  40.67
Difference:          15.03
```

This is descriptive.

Do not infer:

> "`<unk>` causes a 15-point BLEU loss."

The affected subset may also contain:

- more difficult vocabulary;
- longer sentences;
- unusual names;
- harder lexical content;
- other translation errors.

A safe statement is:

> **"Outputs containing `<unk>` had much lower BLEU descriptively, but the subsets differ in content and difficulty, so the gap should not be interpreted causally."**

---

# 34. Why Manual Replacement Was Rejected

One tempting solution would be to create hand-written substitutions such as:

```text
<unk>驼 -> 骆驼
草<unk> -> 草莓
<unk>果 -> 苹果
```

This was rejected.

Reasons:

1. it uses knowledge gained after inspecting the output;
2. it changes the model prediction manually;
3. it can artificially improve evaluation metrics;
4. it introduces inconsistent human intervention;
5. it undermines the frozen-system comparison.

Therefore:

> **The original 4,200 Direct predictions remain unchanged.**

---

# 35. Why the Main Results Should Not Be Replaced

The original experiment was defined before the `<unk>` analysis:

```text
fixed model
fixed revision
fixed dataset
fixed decoding settings
no fine-tuning
no accent adaptation
```

The post-hoc experiments were motivated by observing an error in the completed result.

Replacing the original outputs with an intervention selected after seeing the test set would change the experimental protocol.

The correct structure is:

```text
Main result
    =
original frozen system

Additional analysis
    =
post-hoc diagnostic and sensitivity experiments
```

not:

```text
Main result
    =
whichever post-hoc setting scores better
```

---

# 36. Recommended Final Reporting Structure

## Main experiment

Keep:

```text
SeamlessM4T v2-large
greedy decoding
original 4,200 outputs
```

unchanged.

Report:

```text
508 / 4,200 Direct outputs contained literal <unk>
= 12.1%
```

---

## Qualitative failure analysis

Explain:

- recurring literal marker;
- sentence/content consistency;
- examples;
- lower descriptive BLEU for affected subset.

---

## Sensitivity analysis

Briefly report:

1. special UNK-token suppression did not change outputs;
2. generated sequences contained no special UNK token IDs;
3. the visible marker was spelled using ordinary tokens;
4. beam search removed the marker in only 1/35 affected samples;
5. exact literal sequence blocking produced `<unk >` variants and worsened metrics.

---

# 37. Recommended Paper / Report Wording

## Detailed version

> **The Direct system produced a literal `<unk>` marker in 508 of 4,200 translations (12.1%). Token-level inspection showed that these markers were not generated through SeamlessM4T's special unknown-token ID; instead, the model composed the visible string using ordinary tokens. A post-hoc sensitivity analysis therefore tested both special-UNK suppression and constrained decoding. Suppressing the special UNK token had no effect. Blocking the ordinary token sequences spelling `<unk>` removed that exact surface form, but the model generated an alternative `<unk >` form and translation quality deteriorated substantially. These results indicate that simple decoding constraints do not provide a reliable mitigation, so the original frozen-system outputs were retained for the main evaluation.**

---

## Compact version

> **SeamlessM4T produced `<unk>` in 12.1% of Direct outputs. The marker was generated using ordinary tokens rather than the model's special UNK token. Special-token suppression had no effect, while blocking the literal sequence caused alternative `<unk >` output and lower translation scores.**

---

## Very short slide version

> **Direct `<unk>` failure: 508/4,200 outputs (12.1%). Token-level analysis showed `<unk>` was spelled with normal tokens; decoding constraints did not reliably fix it.**

---

# 38. Recommended Q&A Answer

### Q: Why did SeamlessM4T output `<unk>`?

> **We confirmed that it was not simply generating the tokenizer's special UNK token. The model was spelling the visible `<unk>` string using ordinary tokens. Repeated sentences often showed the same behaviour across speakers, which suggests a model/content-related generation pattern. We have not proven the exact internal neural cause.**

---

### Q: Did you try to fix it?

> **Yes. We tested special-UNK suppression, beam search, and blocking the ordinary token sequence that spelled `<unk>`. Special-token suppression had no effect, beam search only removed it in one of 35 affected test samples, and literal-sequence blocking caused the model to generate an alternative `<unk >` form and substantially reduced translation scores.**

---

### Q: Why not just replace `<unk>` manually?

> **That would modify predictions after seeing the evaluation results and could bias the comparison. We kept the frozen model outputs unchanged and treated the mitigation experiments separately.**

---

### Q: Is this caused by accent?

> **The marker appeared in every accent group, with affected rates from about 10.3% to 13.5%. Repeated sentences were also highly consistent across speakers, so the marker does not appear to be purely accent-specific. However, our analysis does not prove that accent has no contribution.**

---

### Q: Is `<unk>` caused by missing Chinese vocabulary?

> **The tested Chinese words could be represented by the tokenizer without the special UNK ID. In addition, the visible marker itself was produced using ordinary tokens. So a simple missing-character explanation is not supported by our diagnostics.**

---

# 39. Recommended Future Work

The current experiments are enough to conclude that simple blocking is not a good solution.

If more investigation is needed, possible future work includes:

## 39.1 Reproduce sensitivity analysis on original hardware

Run selected diagnostics on:

```text
Tesla T4
CUDA
FP16
```

to remove the CPU/FP32 reproducibility limitation.

---

## 39.2 Use robust UNK-like detection

Replace exact:

```python
"<unk>" in text
```

with something like:

```python
re.search(
    r"<\s*unk\s*>",
    text,
    flags=re.IGNORECASE,
)
```

and record:

- exact `<unk>`;
- spaced variants;
- count per output;
- repeated/degenerate markers.

---

## 39.3 Inspect decoder probabilities

A deeper analysis could inspect:

- token probabilities before the marker;
- alternative top-k tokens;
- whether the model has valid Chinese alternatives with slightly lower probability;
- how beam search changes the local ranking.

This would help distinguish:

- low-confidence lexical uncertainty;
- learned textual fallback;
- search error.

This was **not yet performed**.

---

## 39.4 Compare another Direct model

A different Direct ST model could determine whether this behaviour is:

- SeamlessM4T-specific;
- common across Direct ST models.

This would create an additional system and should be framed as a new experiment.

---

## 39.5 Fine-tuning

Targeted fine-tuning may potentially change the behaviour because it updates model weights.

However, this would be a fundamentally different system from the current frozen-pretrained benchmark.

It should not be mixed into the existing main result.

---

## 39.6 Hybrid repair system

A secondary translation model or LLM could potentially repair outputs containing `<unk>`.

Example:

```text
Seamless Direct output
    ↓
detect UNK-like marker
    ↓
secondary repair model
    ↓
revised translation
```

But this becomes a new hybrid architecture.

It is not a clean fix to the existing Direct model and would require separate evaluation.

---

# 40. Current Decision

For the current COMPSCI 760 project:

## Keep

- the original 4,200 Direct predictions;
- the original Direct evaluation metrics;
- the `<unk>` outputs as genuine model outputs;
- the qualitative error analysis.

## Report

- 508 / 4,200 affected;
- 599 literal occurrences;
- repeated-sentence consistency;
- tokenizer diagnostic;
- special-UNK suppression failure;
- beam-search sensitivity;
- literal-sequence-blocking failure.

## Do not

- manually replace `<unk>`;
- silently rerun and replace the main results;
- claim a confirmed internal cause;
- claim the tokenizer cannot represent the tested Chinese words;
- claim accent causes the marker;
- claim the literal-blocking experiment solved it.

---

# 41. Chronological Investigation Timeline

## Stage 1 — Original evaluation

The frozen Direct model generated all 4,200 translations.

Unexpected literal `<unk>` strings were noticed in qualitative review.

---

## Stage 2 — Initial counting

The outputs were systematically scanned.

Result:

```text
508 / 4,200 affected
599 total literal occurrences
```

---

## Stage 3 — Descriptive analysis

The investigation compared:

- accent groups;
- source length;
- audio duration;
- generated-token count;
- runtime;
- repeated sentences.

The repeated-sentence analysis suggested strong content consistency.

---

## Stage 4 — External search

Similar Mandarin `<unk>` behaviour was found in Meta's Seamless repository.

Meta's official inference code also exposed UNK blocking, motivating a controlled suppression test.

---

## Stage 5 — Tokenizer analysis

The exact processor/tokenizer was loaded.

Result:

```text
UNK token = <unk>
UNK ID = 1
```

Selected suspicious Chinese words encoded without UNK ID `1`.

The reference-tokenizer analysis initially looked alarming but was later identified as largely punctuation-driven.

---

## Stage 6 — Environment troubleshooting

Problems fixed:

1. expired Hugging Face OAuth token;
2. missing `protobuf`;
3. duplicate Pandas diagnostic columns;
4. local MP3 decoding backend issue.

---

## Stage 7 — Special UNK suppression

A 35-sample balanced sensitivity set was tested.

Result:

```text
generated special UNK IDs = 0
```

Suppressing ID `1` had no effect.

---

## Stage 8 — Beam search

Beam-5 was tested.

Result:

```text
affected count: 35 -> 34
```

Small metric improvement, much higher runtime, no general fix.

---

## Stage 9 — Generated-token inspection

The key discovery was made:

```text
<unk>
```

was spelled by ordinary token sequences.

Observed:

```text
[249371, 2105, 248948]
[9614,   2105, 248948]
```

---

## Stage 10 — Literal-sequence blocking

Those sequences were prohibited with `bad_words_ids`.

The exact `<unk>` spelling disappeared.

However, all 35 outputs produced:

```text
<unk >
```

instead.

The model used alternative sequences and quality deteriorated.

---

## Stage 11 — Final conclusion

Simple decoding suppression is not a reliable solution.

The main frozen output remains unchanged.

---

# 42. Experiment Artifact Inventory

## Original Direct pipeline

```text
03_direct_pipeline.ipynb
direct_predictions.csv
direct_runtime.csv
run_config.json
run_environment.json
run_summary.json
```

---

## Diagnostic investigation

```text
05_direct_unk_diagnostic.ipynb

accent_unk_summary.csv
all_direct_unk_rows.csv
diagnostic_summary.json
manual_tokenizer_tests.csv
repeated_sentence_unk_summary.csv
unk_count_distribution.csv
unk_vs_nonunk_numeric_summary.csv
```

---

## Sensitivity experiment 1

```text
06_direct_unk_sensitivity.ipynb

greedy_unk_blocking_changes.csv
side_by_side_outputs.csv
translation_metrics_by_condition.csv
unk_rate_by_condition.csv
unk_sensitivity_predictions.csv
run_summary(1).json
```

---

## Sensitivity experiment 2

```text
07_direct_literal_unk_blocking_sensitivity.ipynb

baseline_rerun.csv
discovered_literal_unk_sequences.csv
literal_unk_blocked_predictions.csv
manual_review_changed_outputs.csv
side_by_side_comparison.csv
translation_metric_comparison.csv
unk_rate_comparison.csv
run_summary.json
```

---

# 43. Key Numerical Results in One Place

## Full original Direct dataset

```text
Total clips:                    4,200
Affected clips:                   508
Affected rate:                  12.10%
Literal <unk> occurrences:         599
Generation-limit flags:              0
```

---

## `<unk>` count distribution

```text
0 markers: 3,692 clips
1 marker:    434 clips
2 markers:     60 clips
3 markers:     11 clips
4 markers:      3 clips
```

---

## Accent-rate range

```text
Lowest:
Hong Kong English = 10.33%

Highest:
England English = 13.50%
```

---

## Repeated sentences

```text
Never <unk>:  256
Always <unk>:  43
Mixed:          2

Among repeated sentences affected at least once:
43 / 45 = 95.6% always affected
```

---

## Sensitivity experiment 1

```text
n = 35

Baseline greedy:
35 / 35 literal <unk>

Special UNK blocked:
35 / 35 literal <unk>

Beam-5:
34 / 35 literal <unk>

Beam-5 + special UNK blocked:
34 / 35 literal <unk>

Generated special UNK IDs:
0
```

---

## Ordinary literal sequences discovered

```text
[249371, 2105, 248948] = ['<', 'unk', '>']   -> 37
[9614,   2105, 248948] = ['▁<', 'unk', '>']  -> 2

Total:
39
```

---

## Sensitivity experiment 2

```text
n = 35

Exact <unk> after block:
0 / 35

Any <unk>-like marker using whitespace-aware regex:
35 / 35

Alternative <unk > occurrences:
210 total

Worst case:
85 occurrences in one output
```

---

## Metric change after literal blocking

```text
BLEU:
28.19 -> 15.52
change = -12.67

chrF:
24.85 -> 19.15
change = -5.70

chrF++:
18.86 -> 14.49
change = -4.38
```

---

# 44. Final Research Interpretation

The investigation supports the following chain of evidence:

```text
Visible <unk> observed
        ↓
not strongly concentrated by accent
        ↓
repeated sentences show highly consistent behaviour
        ↓
tested Chinese words can be tokenized without special UNK
        ↓
generated sequences contain zero special UNK IDs
        ↓
visible <unk> is spelled with ordinary tokens
        ↓
special-token suppression cannot affect it
        ↓
beam search only helps rarely
        ↓
blocking the literal spelling causes <unk > variants
        ↓
translation quality becomes worse
        ↓
simple decoding constraint is not a reliable fix
```

The final scientifically defensible position is:

> **Treat `<unk>` as an observed SeamlessM4T Direct-system generation failure, preserve the original frozen predictions, and report the unsuccessful mitigation experiments as sensitivity analysis rather than modifying the benchmark output.**

---

# 45. Final One-Paragraph Record

> In the completed 4,200-sample Direct SeamlessM4T v2-large evaluation, 508 translations (12.1%) contained literal `<unk>`, totalling 599 occurrences. Descriptive accent rates ranged from 10.3% to 13.5%, while repeated-source analysis showed that 43 of 45 repeated sentences affected at least once were affected every time, suggesting strong content/model consistency. Tokenizer checks showed that selected problematic Chinese lexical items could be represented without the model's special UNK ID. A 35-clip balanced sensitivity experiment then showed that the generated outputs contained zero special UNK token IDs; instead, literal `<unk>` was composed from ordinary token sequences. Suppressing the special UNK ID therefore had no effect, and beam-5 reduced the affected count only from 35 to 34. A second constrained-decoding experiment blocked the ordinary token sequences spelling `<unk>`. Although the exact `<unk>` string disappeared, all 35 outputs generated an alternative `<unk >` form, including one severely repetitive output, and BLEU dropped from 28.19 to 15.52. The evidence therefore does not support a simple vocabulary, special-token, generation-limit, or exact-sequence solution. The original frozen Direct outputs should remain unchanged, with `<unk>` reported as a model-generation failure mode and the mitigation experiments reported separately as post-hoc sensitivity analyses.

---

# 46. Notes on Evidence Strength

## Directly demonstrated by experiment

- 508 / 4,200 original outputs contain exact `<unk>`.
- 599 total exact occurrences.
- accent-group descriptive rates.
- repeated-sentence pattern counts.
- tested Chinese words do not use special UNK ID.
- special UNK ID is `1`.
- special UNK ID did not occur in the selected generated sequences.
- special UNK suppression did not change the selected outputs.
- the literal marker was composed from ordinary tokens.
- beam-5 removed exact `<unk>` in only 1/35 selected samples.
- blocking the two exact literal sequences led to `<unk >` alternatives.
- all 35 constrained outputs still contained a whitespace-variant UNK-like marker.
- constrained decoding substantially reduced BLEU/chrF/chrF++.

## Supported interpretation, but not a proven internal mechanism

- the issue appears more content/model-related than purely accent-specific;
- the behaviour appears to be a learned/fallback generation pattern;
- uncertainty about lexical generation may be involved.

## Not established

- exact neural cause;
- exact training-data origin;
- whether one architectural component is solely responsible;
- whether all SeamlessM4T deployment paths behave identically;
- whether fine-tuning would solve the issue;
- whether another Direct ST model would show the same behaviour.

---

# 47. Research Integrity Checklist

Before using the `<unk>` analysis in the final report or presentation:

- [x] Preserve original 4,200 outputs.
- [x] Keep sensitivity outputs separate.
- [x] Record exact model revision.
- [x] Record decoding settings.
- [x] Record hardware mismatch in small sensitivity experiments.
- [x] Distinguish exact `<unk>` from whitespace variants.
- [x] Avoid claiming the tokenizer cannot represent tested Chinese words.
- [x] Avoid claiming special UNK token generation.
- [x] Avoid claiming a confirmed internal cause.
- [x] Avoid manually repairing translations.
- [x] Describe beam search result as sensitivity, not replacement.
- [x] Describe literal blocking as unsuccessful.
- [x] Report metric degradation after literal blocking.
- [x] Keep conclusions descriptive and evidence-based.

---

# 48. Suggested Repository Location

A suitable location for this investigation record is:

```text
docs/unk_investigation.md
```

or:

```text
analysis/unk_investigation.md
```

The three notebooks can remain under:

```text
notebooks/
```

For example:

```text
notebooks/
├── 03_direct_pipeline.ipynb
├── 05_direct_unk_diagnostic.ipynb
├── 06_direct_unk_sensitivity.ipynb
└── 07_direct_literal_unk_blocking_sensitivity.ipynb

docs/
└── unk_investigation.md
```

---

# 49. External References

1. Meta Seamless Communication issue reporting frequent `<unk>` output for Mandarin/Cantonese:  
   <https://github.com/facebookresearch/seamless_communication/issues/168>

2. Meta Seamless inference code containing the `--text_unk_blocking` option:  
   <https://github.com/facebookresearch/seamless_communication/blob/main/src/seamless_communication/cli/m4t/predict/predict.py>

These external references are used as corroborating context only. The conclusions in this investigation are based primarily on the project's own generated outputs and sensitivity experiments.

---

# 50. Final Status

**Current status:** investigation complete enough for reporting.

**Confirmed practical result:**

> There is currently **no validated simple decoding fix** for the observed `<unk>` behaviour in this project's frozen SeamlessM4T Direct system.

**Recommended action:**

> Keep the original Direct results, document the phenomenon and the failed mitigations, and move forward with the main accent-robustness analysis.

