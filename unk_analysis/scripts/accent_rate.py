"""Direct <unk> rate by accent: speaker-cluster bootstrap CIs + logistic regression.
Inputs : runs/merged_3system_with_metrics.csv in the repository (or the path given as 1st argument); runs/direct_full_run_1788151795/direct_predictions.csv (2nd argument) for the speaker id
Outputs: unk_by_accent_ci.csv, unk_logit.csv, unk_by_accent.png
Seed 760, 1,000 resamples (same as the action plan).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # the unk_analysis folder
MERGED = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "runs" / "merged_3system_with_metrics.csv"   # the evaluation table shared by the group
if not MERGED.exists():
    sys.exit(f"Input not found: {MERGED}. Run from a clone of the repository (the table is runs/merged_3system_with_metrics.csv), or pass its path as the first argument.")
OUT = ROOT / "results" / "accent"; OUT.mkdir(parents=True, exist_ok=True)
import numpy as np, pandas as pd, statsmodels.formula.api as smf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

DIRECT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT.parent / "runs" / "direct_full_run_1788151795" / "direct_predictions.csv"   # has the speaker id
d = pd.read_csv(MERGED)
spk = pd.read_csv(DIRECT, usecols=["id", "sample_id"]).rename(columns={"sample_id": "spk"})
d = d.merge(spk, on="id", validate="1:1")
assert len(d) == 4200 and d.spk.nunique() == 1586
d["unk"] = d.direct_has_unk.astype(int)
d["words"] = d.sentence.str.split().str.len()
short = {a: a.split(" (")[0] for a in d.primary_accent.unique()}
d["accent"] = d.primary_accent.map(short)

# ---- 1. rate + speaker-cluster bootstrap CI
rng = np.random.default_rng(760)
def boot_ci(sub, B=1000):
    codes, uniq = pd.factorize(sub.spk); g = len(uniq); y = sub.unk.values
    idx = [np.where(codes == i)[0] for i in range(g)]
    r = [y[np.concatenate([idx[i] for i in rng.integers(0, g, g)])].mean() for _ in range(B)]
    return np.percentile(r, [2.5, 97.5])
rows = []
for name, sub in [("All accents", d)] + list(d.groupby("accent")):
    lo, hi = boot_ci(sub)
    rows.append(dict(accent=name, n_clips=len(sub), n_speakers=sub.spk.nunique(), n_unk=sub.unk.sum(),
                     unk_rate_pct=100 * sub.unk.mean(), ci_low_pct=100 * lo, ci_high_pct=100 * hi))
ci = pd.DataFrame(rows).round(2); ci.to_csv(OUT / "unk_by_accent_ci.csv", index=False); print(ci.to_string(index=False))

# ---- 2. does accent matter? logistic regression, cluster-robust SEs
ref = "United States English"
out = []
def fit(formula, label, cluster):
    m = smf.logit(formula, d).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    accent_terms = [t for t in m.params.index if t.startswith("C(accent")]
    w = m.wald_test(" , ".join(f"{t} = 0" for t in accent_terms), scalar=True)
    out.append(dict(model=label, cluster=cluster, accent_joint_wald_chi2=float(w.statistic), df=len(accent_terms),
                    accent_joint_p=float(w.pvalue), words_OR_per_word=np.exp(m.params.get("words", np.nan)),
                    words_p=m.pvalues.get("words", np.nan)))
for cl in ["spk", "sentence"]:
    fit(f"unk ~ C(accent, Treatment('{ref}'))", "accent only", cl)
    fit(f"unk ~ C(accent, Treatment('{ref}')) + words", "accent + sentence length (words)", cl)
res = pd.DataFrame(out).round(4); res.to_csv(OUT / "unk_logit.csv", index=False); print(); print(res.to_string(index=False))

# ---- 3. length effect, simple view
d["len_bin"] = pd.cut(d.words, [0, 5, 8, 11, 15, 100], labels=["1-5", "6-8", "9-11", "12-15", "16+"])
lb = d.groupby("len_bin", observed=True).unk.agg(["mean", "size"]); print(); print((lb["mean"] * 100).round(1).to_dict())

# ---- figure
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
c = ci[ci.accent != "All accents"].sort_values("unk_rate_pct")
y = np.arange(len(c)); allr = ci[ci.accent == "All accents"].iloc[0]
ax[0].axvspan(allr.ci_low_pct, allr.ci_high_pct, color="#cfd8e3", alpha=.6, label=f"All accents {allr.unk_rate_pct:.1f}% (95% CI)")
ax[0].errorbar(c.unk_rate_pct, y, xerr=[c.unk_rate_pct - c.ci_low_pct, c.ci_high_pct - c.unk_rate_pct], fmt="o", color="#1f4e79", capsize=3)
ax[0].set_yticks(y); ax[0].set_yticklabels(c.accent); ax[0].set_xlabel("Clips with <unk> (%)"); ax[0].set_xlim(0, 20)
ax[0].set_title("Direct <unk> rate by accent (95% speaker-cluster CI)", fontsize=10); ax[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False)
ax[1].bar(lb.index.astype(str), lb["mean"] * 100, color="#1f4e79")
for i, (m_, n_) in enumerate(zip(lb["mean"], lb["size"])): ax[1].text(i, m_ * 100 + .3, f"{m_*100:.1f}%\nn={n_}", ha="center", fontsize=8)
ax[1].set_xlabel("Source sentence length (words)"); ax[1].set_ylabel("Clips with <unk> (%)"); ax[1].set_ylim(0, 20)
ax[1].set_title("<unk> rate by sentence length", fontsize=10)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT / "unk_by_accent.png", dpi=160)
