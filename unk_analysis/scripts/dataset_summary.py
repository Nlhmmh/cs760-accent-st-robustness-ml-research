"""Describe accent-label multiplicity and gender labels in the frozen sample.

Input: ../data/final_sample/final_sample_600_per_group.csv, or argv[1].
Outputs: results/data/dataset_diagnostics_summary.csv, gender_by_accent.csv.
These describe clip metadata, not verified speaker gender or accent identity.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (Path(sys.argv[1]) if len(sys.argv) > 1 else
          ROOT.parent / "data" / "final_sample" / "final_sample_600_per_group.csv")
if not SOURCE.exists():
    sys.exit(f"Input not found: {SOURCE}; pass the frozen metadata CSV as the first argument.")
OUT = ROOT / "results" / "data"
OUT.mkdir(parents=True, exist_ok=True)
d = pd.read_csv(SOURCE)
labels_per_clip = d.accents.fillna("").map(
    lambda value: len([part for part in value.split("|") if part.strip()]))
male = d.gender.isin(["male", "male_masculine"])
gender = d.assign(male_label=male).groupby("primary_accent").agg(
    clips=("male_label", "size"), male_labeled_clips=("male_label", "sum"))
gender["male_pct"] = (100 * gender.male_labeled_clips / gender.clips).round(4)
gender.to_csv(OUT / "gender_by_accent.csv")
summary = pd.DataFrame([
    ("clips", len(d)),
    ("clips listing multiple accents (pipe-delimited)", int((labels_per_clip > 1).sum())),
    ("male-labeled clips, all groups", int(male.sum())),
    ("minimum male-label proportion across groups (%)", round(gender.male_pct.min(), 1)),
    ("maximum male-label proportion across groups (%)", round(gender.male_pct.max(), 1)),
], columns=["measure", "value"], dtype=object)
summary.to_csv(OUT / "dataset_diagnostics_summary.csv", index=False)
print(summary.to_string(index=False)); print(); print(gender.to_string())
