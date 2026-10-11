"""Direct <unk>: proper nouns / rare words? (tests the action plan's Q8 guess "proper nouns strongest")
Sentence-level features from spaCy (POS, named entities) and wordfreq (Zipf frequency).
Outputs: unk_wordtype_rates.csv, unk_wordtype_logit.csv, unk_wordtype.png.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # the unk_analysis folder
MERGED = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "runs" / "evaluation_results" / "merged_3system_with_metrics.csv"   # the evaluation table shared by the group
if not MERGED.exists():
    sys.exit(f"Input not found: {MERGED}. Run from a clone of the repository (the table is runs/evaluation_results/merged_3system_with_metrics.csv), or pass its path as the first argument.")
OUT = ROOT / "results" / "word_type"; OUT.mkdir(parents=True, exist_ok=True)
import numpy as np, pandas as pd, spacy, statsmodels.formula.api as smf
from wordfreq import zipf_frequency
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

d = pd.read_csv(MERGED)
d["unk"] = d.direct_has_unk.astype(int)
d["words"] = d.sentence.str.split().str.len()

nlp = spacy.load("en_core_web_sm")
ENT = {"PERSON", "GPE", "ORG", "LOC", "NORP", "FAC", "EVENT", "WORK_OF_ART", "PRODUCT", "LANGUAGE"}
feat = {}
for s, doc in zip(d.sentence.unique(), nlp.pipe(d.sentence.unique(), batch_size=256)):
    content = [t for t in doc if t.pos_ in {"NOUN", "VERB", "ADJ", "ADV"} and t.is_alpha]
    z = lambda ts: min((zipf_frequency(t.lemma_.lower(), "en") for t in ts), default=np.nan)
    feat[s] = dict(has_propn=int(any(t.pos_ == "PROPN" for t in doc)),
                   has_entity=int(any(e.label_ in ENT for e in doc.ents)),
                   min_zipf_content=z(content))
F = pd.DataFrame.from_dict(feat, orient="index"); d = d.join(F, on="sentence")
d["min_zipf_content"] = d.min_zipf_content.fillna(d.min_zipf_content.median())
d["rare"] = pd.cut(d.min_zipf_content, [-1, 2.5, 3.0, 3.5, 4.0, 10], labels=["<=2.5 (very rare)", "2.5-3", "3-3.5", "3.5-4", ">4 (common)"])
d["sid"] = pd.factorize(d.sentence)[0]
print("unique sentences:", d.sid.nunique(), "| clips with proper noun:", d.has_propn.sum(), "| with entity:", d.has_entity.sum())

# ---- descriptive rates
rows = []
def add(name, grp):
    for k, g in grp:
        rows.append(dict(feature=name, level=str(k), n_clips=len(g), n_unk=g.unk.sum(), unk_rate_pct=round(100 * g.unk.mean(), 1)))
add("has proper noun (spaCy PROPN)", d.groupby("has_propn")); add("has named entity", d.groupby("has_entity"))
add("rarest content word (Zipf)", d.groupby("rare", observed=True))
R = pd.DataFrame(rows); R.to_csv(OUT / "unk_wordtype_rates.csv", index=False); print(R.to_string(index=False))

# ---- logistic regression, cluster-robust by sentence (repeated sentences)
def fit(f, label, data=d):
    m = smf.logit(f, data).fit(disp=0, cov_type="cluster", cov_kwds={"groups": data.sid.values})
    ci = m.conf_int(); o = pd.DataFrame({"model": label, "term": m.params.index, "odds_ratio": np.exp(m.params.values),
        "ci_low": np.exp(ci[0].values), "ci_high": np.exp(ci[1].values), "p": m.pvalues.values}); return o[o.term != "Intercept"]
u = d.groupby("sid").agg(unk=("unk", "max"), words=("words", "first"), has_propn=("has_propn", "first"),
                         has_entity=("has_entity", "first"), min_zipf_content=("min_zipf_content", "first")).reset_index()
out = pd.concat([
    fit("unk ~ words", "A. length only"),
    fit("unk ~ words + has_propn", "B. + proper noun"),
    fit("unk ~ words + has_entity", "C. + named entity"),
    fit("unk ~ words + min_zipf_content", "D. + rarest content word"),
    fit("unk ~ words + has_propn + min_zipf_content", "E. all together"),
    fit("unk ~ words + has_propn + min_zipf_content", "F. all together, one row per unique sentence (unk = any)", u),
]).round(4)
out.to_csv(OUT / "unk_wordtype_logit.csv", index=False); print(); print(out.to_string(index=False))

# ---- examples
print("\nrarest-word sentences WITHOUT unk (zipf<2.5):", ((d.min_zipf_content < 2.5) & (d.unk == 0)).sum(), "| WITH unk:", ((d.min_zipf_content < 2.5) & (d.unk == 1)).sum())
print("zipf of rarest content word, mean: unk", round(d[d.unk == 1].min_zipf_content.mean(), 2), "| no unk", round(d[d.unk == 0].min_zipf_content.mean(), 2))

# ---- figure
fig, ax = plt.subplots(1, 2, figsize=(11, 4), gridspec_kw={"width_ratios": [1, 1.5]})
p = R[R.feature == "has proper noun (spaCy PROPN)"]
ax[0].bar(["No proper noun", "Has proper noun"], p.unk_rate_pct, color="#1f4e79")
for i, r in enumerate(p.itertuples()): ax[0].text(i, r.unk_rate_pct + .3, f"{r.unk_rate_pct}%\nn={r.n_clips}", ha="center", fontsize=8)
ax[0].set_ylim(0, 36); ax[0].set_ylabel("Clips with <unk> (%)"); ax[0].set_title("Proper nouns in the English sentence", fontsize=10)
q = R[R.feature == "rarest content word (Zipf)"]
ax[1].bar(q.level, q.unk_rate_pct, color="#1f4e79")
for i, r in enumerate(q.itertuples()): ax[1].text(i, r.unk_rate_pct + .3, f"{r.unk_rate_pct}%\nn={r.n_clips}", ha="center", fontsize=8)
ax[1].set_ylim(0, 36); ax[1].set_xlabel("Zipf frequency of the rarest content word (higher = more common)")
ax[1].set_title("Rarest word in the sentence", fontsize=10); ax[1].tick_params(axis="x", labelsize=8)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT / "unk_wordtype.png", dpi=160)
