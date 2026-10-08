"""Direct <unk>: what kind of English words trigger it? (follow-up to the word-removal test, notebooks/4_word_removal.ipynb)
Inputs : results/word_removal/occlusion_sentences.csv and occlusion_words.csv (written by notebooks/4_word_removal.ipynb)
Outputs: unk_trigger_summary.csv, unk_trigger_words.csv, unk_trigger.png
Sentence-level bootstrap (seed 760, 1,000 resamples) for the main comparisons.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # the unk_analysis folder
OUT = ROOT / "results" / "word_removal"; OUT.mkdir(parents=True, exist_ok=True)
import re
import numpy as np, pandas as pd, spacy
from scipy import stats
from wordfreq import zipf_frequency
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

S = pd.read_csv(OUT / "occlusion_sentences.csv"); W = pd.read_csv(OUT / "occlusion_words.csv")
A = S[S.unk_start_pos.notna()].copy()
W = W[W.sid.isin(A.sid)].merge(A[["sid", "sentence"]], on="sid")

# ---- POS for each whitespace word (map spaCy tokens onto whitespace words by character offsets)
nlp = spacy.load("en_core_web_sm")
pos_rows = []
for sid, sent in zip(A.sid, A.sentence):
    doc = nlp(sent); off = 0
    for i, w in enumerate(sent.split()):
        start = sent.index(w, off); end = start + len(w); off = end
        toks = [t for t in doc if t.idx >= start and t.idx + len(t) <= end and t.is_alpha]
        pos = "PROPN" if any(t.pos_ == "PROPN" for t in toks) else (toks[0].pos_ if toks else "OTHER")
        stop = bool(toks) and all(t.is_stop for t in toks)
        pos_rows.append(dict(sid=sid, word_index=i, pos=pos, is_stop=stop, first_in_sentence=(i == 0), capitalised=w[:1].isupper()))
W = W.merge(pd.DataFrame(pos_rows), on=["sid", "word_index"])

def zipf(w):
    parts = [p for p in re.split(r"[^A-Za-z']+", w) if p]
    return min((zipf_frequency(p.lower(), "en") for p in parts), default=np.nan)
W["zipf"] = W.word.map(zipf)
rank = W.groupby("sid").importance.rank(ascending=False, method="first")
W["is_trigger"] = rank == 1
W["rank_in_sentence"] = rank
W.to_csv(OUT / "unk_trigger_words.csv", index=False)

T = W[W.is_trigger]; O_all = W[~W.is_trigger]
O = O_all[~O_all.is_stop]        # baseline: other content words (non-stop); function words (the, of, a ...) are very common and would exaggerate every contrast
rows = []
def add(name, value, extra=""): rows.append(dict(measure=name, value=value, note=extra))

# ---- 1. rarity
add("trigger words: median Zipf frequency", T.zipf.median(), "higher = more common")
add("other content words in the same sentences: median Zipf frequency", O.zipf.median())
add("  (for reference) ALL other words incl. function words: median Zipf frequency", O_all.zipf.median())
# paired: trigger vs median of the other words in its own sentence
pair = T.set_index("sid").zipf.to_frame("t").join(O.groupby("sid").zipf.median().rename("o")).dropna()
add("share of sentences where the trigger is rarer than the median of the other CONTENT words", (pair.t < pair.o).mean(), f"n={len(pair)}; Wilcoxon p={stats.wilcoxon(pair.t, pair.o).pvalue:.2g}")
content = W[(~W.is_stop) & W.zipf.notna()]
rarest = content.loc[content.groupby("sid").zipf.idxmin()][["sid", "word_index"]].assign(rarest=True)
tm = T.merge(rarest, on=["sid", "word_index"], how="left"); tm["rarest"] = tm.rarest.fillna(False).astype(bool)
add("share of sentences where the trigger IS the rarest non-stop word", tm.rarest.mean())
# chance level for that: 1 / number of non-stop words
chance = (1 / content.groupby("sid").size()).reindex(T.sid).mean()
add("  chance level (pick a random non-stop word)", chance)
# importance vs rarity inside each sentence
rho = [stats.spearmanr(g.importance, g.zipf)[0] for _, g in W[~W.is_stop].groupby("sid") if g.zipf.nunique() > 2]   # content words only
add("mean within-sentence Spearman, content words only: importance vs Zipf (negative = rarer words matter more)", float(np.nanmean(rho)), f"n sentences={len(rho)}")

# ---- 2. word class
add("proper noun (PROPN) share: trigger words", (T.pos == "PROPN").mean())
add("proper noun (PROPN) share: other content words", (O.pos == "PROPN").mean())
Wc = W[(~W.is_stop) | W.is_trigger]
tab = pd.crosstab(Wc.is_trigger, Wc.pos == "PROPN"); odds, p = stats.fisher_exact(tab.values[::-1, ::-1])
add("odds ratio: being a trigger if the word is a proper noun (content words only)", odds, f"Fisher p={p:.2g} (word level, ignores clustering)")
add("stop-word (function word) share: trigger words", T.is_stop.mean()); add("stop-word share: all other words", O_all.is_stop.mean())
add("capitalised and not first word: trigger words", ((T.capitalised) & (~T.first_in_sentence)).mean()); add("capitalised and not first word: other content words", ((O.capitalised) & (~O.first_in_sentence)).mean())
for pos_ in ["NOUN", "VERB", "ADJ", "PROPN", "ADV", "INTJ"]:
    add(f"share of {pos_} among triggers / among other words", (T.pos == pos_).mean(), f"other content words: {(O.pos == pos_).mean():.3f}")

# ---- 3. sentence-level bootstrap for rarity gap
rng = np.random.default_rng(760); sids = pair.index.values; d = []
for _ in range(1000):
    b = pair.loc[rng.choice(sids, len(sids))]; d.append((b.t - b.o).median())
lo, mid, hi = np.percentile(d, [2.5, 50, 97.5]); add("median Zipf gap (trigger minus other words), bootstrap 95% CI", mid, f"[{lo:.2f}, {hi:.2f}]")

pd.DataFrame(rows).round(3).to_csv(OUT / "unk_trigger_summary.csv", index=False)
print(pd.DataFrame(rows).round(3).to_string(index=False))

print("\nmost frequent trigger words:", T.word.str.strip(".,;:!?\"'()").str.lower().value_counts().head(20).to_dict())
print("\n--- 25 random trigger words with Zipf and POS"); print(T.sample(25, random_state=760)[["word", "pos", "zipf", "importance"]].round(2).to_string(index=False))

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
bins = np.arange(0, 8.01, 0.5)
ax[0].hist(O.zipf.dropna(), bins=bins, density=True, color="#9fb3c8", label="other content words (same sentences)")
ax[0].hist(T.zipf.dropna(), bins=bins, density=True, histtype="step", linewidth=2.2, color="#b3261e", label="trigger word")
ax[0].set_xlabel("Word frequency (Zipf scale, higher = more common)"); ax[0].set_ylabel("Density"); ax[0].legend(fontsize=8, loc="upper left")
ax[0].set_ylim(0, 0.75); ax[0].set_title("Trigger words are rarer than other content words", fontsize=10)
cats = ["NOUN", "PROPN", "VERB", "ADJ", "ADV", "INTJ"]
x = np.arange(len(cats)); w = 0.38
ax[1].bar(x - w / 2, [(O.pos == c).mean() * 100 for c in cats], w, color="#9fb3c8", label="other content words")
ax[1].bar(x + w / 2, [(T.pos == c).mean() * 100 for c in cats], w, color="#b3261e", label="trigger word")
ax[1].set_xticks(x); ax[1].set_xticklabels(cats); ax[1].set_ylabel("Share of words (%)"); ax[1].legend(fontsize=8)
ax[1].set_title("Word class of trigger words", fontsize=10)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT / "unk_trigger.png", dpi=160)
