"""Render archived accent means for the report; no analysis or inference is rerun.

Data: Zhitong's runs/statistical_analysis_results/accent_means_ci.csv.
The plot presents the same comparison as Jidni's Q3 figure, with the accent
order matching the report's quality table and a legend above the intervals.
Run this script with Python and Matplotlib to regenerate accent_means.pdf/png.
"""

import csv
import os
from pathlib import Path
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cs760-matplotlib")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    output_dir = Path(__file__).resolve().parent
    root = output_dir.parents[2]
    source = root / "runs/statistical_analysis_results/accent_means_ci.csv"
    with source.open(newline="", encoding="utf-8") as stream:
        rows = [
            row for row in csv.DictReader(stream)
            if row["statistic"] == "accent_mean" and row["unit"] == "speaker"
        ]
    systems = ("Direct", "Cascade-600M", "Cascade-3.3B")
    assert len(rows) == 21
    values = {(row["accent"], row["system"]): row for row in rows}
    assert len(values) == 21
    accents = sorted(
        {row["accent"] for row in rows},
        key=lambda accent: float(values[accent, "Direct"]["estimate"]),
        reverse=True,
    )
    assert len(accents) == 7
    labels = {
        "England English": "England",
        "Filipino": "Filipino",
        "Hong Kong English": "Hong Kong",
        "India and South Asia (India, Pakistan, Sri Lanka)": "India and S. Asia",
        "Malaysian English": "Malaysian",
        "Southern African (South Africa, Zimbabwe, Namibia)": "Southern African",
        "United States English": "United States",
    }
    assert set(accents) == set(labels)
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "pdf.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(3.5, 2.1))
    for offset, system, colour, marker in zip(
        (-0.22, 0, 0.22), systems,
        ("#216778", "#a97516", "#805493"), ("o", "s", "^")
    ):
        data = [values[accent, system] for accent in accents]
        means = [float(row["estimate"]) for row in data]
        lower = [mean - float(row["ci_low"]) for row, mean in zip(data, means)]
        upper = [float(row["ci_high"]) - mean for row, mean in zip(data, means)]
        assert all(error >= 0 for error in lower + upper)
        ax.errorbar(
            means, [index + offset for index in range(7)],
            xerr=[lower, upper], fmt=marker, color=colour,
            markersize=3, capsize=1.5, linewidth=0.8, label=system,
        )
    ax.set_yticks(range(7), [labels[accent] for accent in accents])
    ax.set_ylim(6.6, -0.6)
    ax.set_xlim(18, 32)
    ax.set_xticks(range(18, 33, 2))
    ax.set_xlabel("Mean sentence chrF++")
    ax.grid(axis="x", color="0.9", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, 0.98),
        bbox_transform=fig.transFigure, ncol=3,
        frameon=False, handlelength=1, handletextpad=0.3,
        columnspacing=0.6, borderaxespad=0,
    )
    fig.subplots_adjust(left=0.36, right=0.95, bottom=0.17, top=0.84)
    fig.savefig(output_dir / "accent_means.pdf")
    fig.savefig(output_dir / "accent_means.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
