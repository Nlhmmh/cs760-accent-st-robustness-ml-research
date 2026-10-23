"""Direct <unk>: counts behind the input-modality results (follow-up to notebooks 1 and 2).
Inputs : results/text_only/text_to_text_predictions.csv (notebook 1), results/special_token/speech_special_unk_check.csv (notebook 2)
Outputs: results/text_only/{text_vs_speech_summary,sentence_marker_consistency}.csv,
         results/special_token/special_token_summary.csv
Marker = case-insensitive <\\s*unk\\s*>, as in the notebooks. Special ID = tokenizer unk_token_id (1), counted by notebook 2.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # the unk_analysis folder
import json
import re
import unicodedata
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

UNK_RE = re.compile(r"<\s*unk\s*>", re.IGNORECASE)
has_unk = lambda col: col.fillna("").astype(str).map(lambda s: bool(UNK_RE.search(s)))

# ---- 1. speech vs text input (all 4,200 clips)
t = pd.read_csv(ROOT / "results" / "text_only" / "text_to_text_predictions.csv")
sp, ref, asr = t.speech_unk.astype(bool), t.text_ref_unk.astype(bool), t.text_asr_unk.astype(bool)
text = pd.DataFrame([
    ("clips", len(t)),
    ("marked, speech input (archived Direct output)", int(sp.sum())),
    ("marked, reference-transcript input", int(ref.sum())),
    ("marked, Whisper-transcript input", int(asr.sum())),
    ("marked with speech and reference transcript", int((sp & ref).sum())),
    ("marked with speech only (vs reference transcript)", int((sp & ~ref).sum())),
    ("marked with reference transcript only", int((~sp & ref).sum())),
    ("unmarked with speech", int((~sp).sum())),
], columns=["measure", "value"])
text.to_csv(ROOT / "results" / "text_only" / "text_vs_speech_summary.csv", index=False)
print(text.to_string(index=False))

# Repeated-content counts. Normalization matches the preprocessing notebook;
# retain original-string counts too so the two grouping definitions are explicit.
def normalize(sentence):
    sentence = re.sub(r"\s+", " ", sentence.strip().lower())
    return re.sub(r"[^\w\s]", "", sentence)

repeat_rows = []
for definition, keys in [("original", t.sentence),
                         ("normalized", t.sentence.map(normalize))]:
    grouped = t.assign(sentence_key=keys, marker=sp).groupby("sentence_key").agg(
        clips=("marker", "size"), marked=("marker", "sum"),
        accent_groups=("primary_accent", "nunique"))
    repeated = grouped[grouped.clips > 1]
    cross = repeated[repeated.accent_groups > 1]
    repeat_rows.append(dict(
        sentence_definition=definition, unique_sentences=len(grouped),
        repeated_sentences=len(repeated), clips_in_repeated_sentences=int(repeated.clips.sum()),
        mixed_marker_sentences=int(((repeated.marked > 0) & (repeated.marked < repeated.clips)).sum()),
        repeated_always_marked=int((repeated.marked == repeated.clips).sum()),
        repeated_never_marked=int((repeated.marked == 0).sum()),
        cross_accent_repeated_sentences=len(cross),
        cross_accent_marked_at_least_once=int((cross.marked > 0).sum()),
        cross_accent_marked_every_recording=int((cross.marked == cross.clips).sum())))
repeat = pd.DataFrame(repeat_rows)
repeat.to_csv(ROOT / "results" / "text_only" / "sentence_marker_consistency.csv", index=False)
print(); print(repeat.to_string(index=False))

# ---- 2. 700-clip speech re-run with token IDs kept
s = pd.read_csv(ROOT / "results" / "special_token" / "speech_special_unk_check.csv")
id1 = s.n_special_unk_ids > 0
vis_rerun, vis_arch = has_unk(s.rerun_translation), has_unk(s.original_translation)
lo, hi = proportion_confint(int(id1.sum()), len(s), method="wilson")
# Stored positions are zero-based indices in the generated sequence, whose
# full length is n_tokens. The CSV does not retain the full token sequence.
penultimate = s.apply(lambda row: int(row.n_tokens) - 2 in json.loads(row.special_unk_positions), axis=1)
def ends_punctuation(value):
    value = str(value).strip()
    return bool(value) and unicodedata.category(value[-1]).startswith("P")
punctuation = s.rerun_translation.fillna("").map(ends_punctuation)
spec = pd.DataFrame([
    ("clips re-run", len(s)),
    ("re-run output identical to archived output", int((s.rerun_translation == s.original_translation).sum())),
    ("visible marker, re-run output", int(vis_rerun.sum())),
    ("visible marker, archived output", int(vis_arch.sum())),
    ("clips with special ID 1", int(id1.sum())),
    ("special ID 1 rate, Wilson 95% CI low (%)", round(100 * lo, 1)),
    ("special ID 1 rate, Wilson 95% CI high (%)", round(100 * hi, 1)),
    ("special ID 1 and visible marker, re-run output", int((id1 & vis_rerun).sum())),
    ("special ID 1 and visible marker, archived output", int((id1 & vis_arch).sum())),
    ("special ID 1 at penultimate generated-token position", int((id1 & penultimate).sum())),
    ("special ID 1 clips with decoded output ending in Unicode punctuation", int((id1 & punctuation).sum())),
    ("clips without special ID 1", int((~id1).sum())),
    ("clips without special ID 1 ending in Unicode punctuation", int((~id1 & punctuation).sum())),
], columns=["measure", "value"], dtype=object)   # object keeps counts as integers next to the rounded rates
spec.to_csv(ROOT / "results" / "special_token" / "special_token_summary.csv", index=False)
print(); print(spec.to_string(index=False))
