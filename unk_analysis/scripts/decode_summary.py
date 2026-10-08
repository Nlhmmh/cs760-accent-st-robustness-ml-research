"""Direct <unk>: decoding probabilities at the step where the model starts to write '<unk>'.
Inputs : results/decode_probs/decode_steps.csv and decode_sentences.csv (written by notebooks/3_decode_probabilities.ipynb)
Outputs: unk_decode_probs_summary.csv, unk_decode_probs.png
Sentence-level bootstrap (seed 760, 1,000 resamples) for the main difference.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # the unk_analysis folder
OUT = ROOT / "results" / "decode_probs"; OUT.mkdir(parents=True, exist_ok=True)
import re
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

st = pd.read_csv(OUT / "decode_steps.csv"); se = pd.read_csv(OUT / "decode_sentences.csv")
st["is_unk_start"] = st.is_unk_start.astype(bool); st = st.merge(se[["sid", "group"]], on="sid")
LT = ("<", "▁<"); han = lambda t: bool(re.search(r"[\u4e00-\u9fff]", str(t)))
U = st[st.is_unk_start].copy(); usids = set(U.sid)
oth_all = st[st.sid.isin(usids) & ~st.is_unk_start].copy()                    # all other steps in the sentences where <unk> was written (includes easy punctuation and function tokens)
oth = oth_all[oth_all.tok.map(han)].copy()                                  # baseline: other steps that write a Chinese character (content positions)
ctl = st[(st.group == "control") & ~st.sid.isin(usids)]                # clean control: never wrote <unk>
ctl_han = ctl[ctl.tok.map(han)]

def best_other(r):
    for k in range(1, 6):
        if getattr(r, f"alt{k}") not in LT: return getattr(r, f"alt{k}"), getattr(r, f"p{k}")
    return None, np.nan
bo = [best_other(r) for r in U.itertuples()]; U["bo_tok"] = [b[0] for b in bo]; U["bo_p"] = [b[1] for b in bo]

def row(name, d):
    return dict(set=name, steps=len(d), sentences=d.sid.nunique(), p_median=d.p_chosen.median(), p_q25=d.p_chosen.quantile(.25), p_q75=d.p_chosen.quantile(.75),
                share_p_gt_0_5=(d.p_chosen > .5).mean(), share_p_gt_0_8=(d.p_chosen > .8).mean(), entropy_median=d.entropy.median())
tab = pd.DataFrame([row("<unk> start steps", U), row("other Chinese-character steps, same sentences (fair baseline)", oth), row("ALL other steps, same sentences (easier, not a fair baseline)", oth_all), row("Chinese-character steps in clean control sentences", ctl_han)])

# sentence-level bootstrap: (statistic at the <unk> step) minus (same statistic at other Chinese-character steps), resampling sentences
rng = np.random.default_rng(760); sids = sorted(usids)
def boot_diff(col, fn):
    gu_ = {s: g[col].values for s, g in U.groupby("sid")}; go_ = {s: g[col].values for s, g in oth.groupby("sid")}; r = []
    for _ in range(1000):
        pick = rng.choice(sids, len(sids)); r.append(fn(np.concatenate([gu_[s] for s in pick])) - fn(np.concatenate([go_[s] for s in pick if s in go_])))
    return np.percentile(r, [2.5, 50, 97.5])
lo, _, hi = boot_diff("p_chosen", np.median); mid = U.p_chosen.median() - oth.p_chosen.median()      # point estimate from the data; bootstrap gives the interval
extra = pd.DataFrame([dict(set="difference in median p (unk step minus other Chinese-character steps)", p_median=mid, p_q25=lo, p_q75=hi)])
extra2 = pd.DataFrame([dict(set="best non-'<' candidate at unk steps", steps=len(U), p_median=U.bo_p.median(),
                            share_p_gt_0_2=(U.bo_p > .2).mean(), share_chinese_char_token=U.bo_tok.map(han).mean())])
# ceiling-free measures (not affected by the ~0.8 probability ceiling): margin over the runner-up, and share within the top-5
for df_ in (U, oth):
    df_["logr"] = np.log10(df_.p1 / df_.p2.clip(lower=1e-12)); df_["conf5"] = df_.p1 / df_[["p1", "p2", "p3", "p4", "p5"]].sum(axis=1); df_["close"] = df_.p2 > df_.p1 / 10
rows = []
for nm, col, fn in [("log10(p1/p2): margin over runner-up", "logr", np.median), ("p1 / (p1..p5): share within top-5", "conf5", np.median), ("runner-up within 10x of top (share)", "close", np.mean)]:
    lo2, _, hi2 = boot_diff(col, fn); md2 = fn(U[col].values) - fn(oth[col].values)
    rows.append(dict(set="ceiling-free: " + nm, p_median=fn(U[col].values), p_q25=fn(oth[col].values), diff_lo=lo2, diff_mid=md2, diff_hi=hi2))
    print(f"{nm:42s} <unk> steps {fn(U[col].values):.3f} | other steps {fn(oth[col].values):.3f} | diff 95% CI [{lo2:.3f}, {hi2:.3f}]")
extra3 = pd.DataFrame(rows).rename(columns={"p_median": "unk_steps", "p_q25": "other_steps"})
pd.concat([tab, extra, extra2, extra3]).round(3).to_csv(OUT / "unk_decode_probs_summary.csv", index=False)
print(tab.round(3).to_string(index=False)); print("diff of medians, 95% CI:", round(lo, 3), round(mid, 3), round(hi, 3))

mx = st.groupby(["sid", "group"]).unk_start_mass.max().reset_index(); mx["wrote"] = mx.sid.isin(usids)
g1 = mx[(mx.group == "unk") & mx.wrote].unk_start_mass; g2 = mx[(mx.group == "unk") & ~mx.wrote].unk_start_mass; g3 = mx[(mx.group == "control") & ~mx.wrote].unk_start_mass

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
bins = np.linspace(0, 1, 21)
ax[0].hist(oth.p_chosen, bins=bins, density=True, color="#9fb3c8", label="other Chinese-character steps (same sentences)")
ax[0].hist(U.p_chosen, bins=bins, density=True, histtype="step", linewidth=2.2, color="#b3261e", label="step where '<unk>' starts")
ax[0].set_xlabel("Probability the model gave to the token it wrote"); ax[0].set_ylabel("Density"); ax[0].legend(fontsize=8, loc="upper left")
ax[0].set_title(f"At '<unk>' the model is less sure (median {U.p_chosen.median():.2f} vs {oth.p_chosen.median():.2f})", fontsize=10)
for g, c, lab in [(g1, "#b3261e", f"unk sentences that wrote '<unk>' (n={len(g1)})"), (g2, "#e0a030", f"unk sentences that did not (n={len(g2)})"), (g3, "#1f4e79", f"control sentences (n={len(g3)})")]:
    x = np.sort(g.values); ax[1].step(x, np.arange(1, len(x) + 1) / len(x), where="post", color=c, linewidth=2, label=lab)
ax[1].set_xscale("symlog", linthresh=0.01); ax[1].set_xlim(0, 1)
ax[1].set_xlabel("Highest probability given to starting '<unk>' at any step (per sentence)"); ax[1].set_ylabel("Share of sentences (cumulative)")
ax[1].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False)
ax[1].set_title("Almost no '<' probability in sentences without <unk>", fontsize=10)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT / "unk_decode_probs.png", dpi=160)
