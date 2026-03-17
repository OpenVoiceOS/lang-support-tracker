#!/usr/bin/env python
"""
Coverage visualization generator.

Reads skills/coverage_data.json and produces 5 PNG plots saved to
skills/plots/. Requires matplotlib and seaborn.

Plots generated:
  1. intent_coverage_heatmap.png  — skill × language, intent coverage %
  2. dialog_coverage_heatmap.png  — skill × language, dialog coverage %
  3. coverage_by_language.png     — horizontal stacked bar per language
  4. combined_heatmap.png         — top 40 skills × language, combined coverage %
  5. intent_vs_dialog_gap.png     — scatter: intent% vs dialog% per skill per language
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


PLOTS_DIR_NAME = "plots"
FIG_DPI = 150
DARK_BG = "#0a0a0b"
CARD_BG = "#111113"
BORDER = "#27272a"
TEXT_COLOR = "#fafafa"
MUTED = "#a1a1aa"
ACCENT = "#22c55e"


def _apply_dark_theme() -> None:
    """Apply OVOS dark theme to matplotlib globals."""
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": CARD_BG,
        "axes.edgecolor": BORDER,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": TEXT_COLOR,
        "grid.color": BORDER,
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        "font.family": "DejaVu Sans",
        "font.size": 9,
    })


def _pct_matrix(
    skills_data: dict,
    lang_order: list[str],
    filetype: str,
    top_n: int = 60,
) -> tuple[np.ndarray, list[str]]:
    """Build a (skills × languages) matrix of coverage percentages.

    Skills with zero source files of the given type are excluded.
    Rows are sorted descending by the sum of coverage across all languages.

    Args:
        skills_data: Per-skill coverage dict from coverage_data.json.
        lang_order: Language codes in column order.
        filetype: File type key (e.g. "intent", "dialog", "voc").
        top_n: Maximum number of skills (rows) to include.

    Returns:
        Tuple of (matrix ndarray shape [n_skills, n_langs], skill_labels list).
    """
    rows = []
    labels = []
    for skill_id, skill in skills_data.items():
        total = skill["totals"].get(filetype, 0)
        if total == 0:
            continue
        row = []
        for lang in lang_order:
            covered = skill["languages"].get(lang, {}).get(filetype, 0)
            row.append(round(covered / total * 100, 1))
        rows.append(row)
        labels.append(skill["display_name"].replace("ovos-skill-", "").replace("ovos-", ""))

    if not rows:
        return np.array([]).reshape(0, len(lang_order)), []

    # Sort by total coverage descending
    order = sorted(range(len(rows)), key=lambda i: sum(rows[i]), reverse=True)
    rows = [rows[i] for i in order[:top_n]]
    labels = [labels[i] for i in order[:top_n]]

    return np.array(rows), labels


def _heatmap(
    matrix: np.ndarray,
    row_labels: list[str],
    col_labels: list[str],
    title: str,
    output_path: Path,
) -> None:
    """Render and save a coverage heatmap.

    Args:
        matrix: 2D float array of percentages (0-100).
        row_labels: Y-axis labels (skills).
        col_labels: X-axis labels (languages).
        title: Figure title.
        output_path: Path to save the PNG.
    """
    if matrix.size == 0:
        print(f"  Skipping {output_path.name}: no data")
        return

    n_rows, n_cols = matrix.shape
    fig_height = max(4, n_rows * 0.25 + 2)
    fig, ax = plt.subplots(figsize=(max(8, n_cols * 1.2), fig_height))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)

    # Color: 0=dark red, 50=amber, 100=green
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "ov_cov", ["#7f1d1d", "#92400e", "#365314", ACCENT]
    )
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=100)

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=7)
    ax.xaxis.tick_top()

    # Annotate cells with % if matrix is not too large
    if n_rows * n_cols <= 300:
        for r in range(n_rows):
            for c in range(n_cols):
                val = matrix[r, c]
                color = "white" if val < 70 else "#0a0a0b"
                ax.text(c, r, f"{val:.0f}", ha="center", va="center",
                        fontsize=6, color=color)

    cbar = fig.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.ax.yaxis.set_tick_params(color=MUTED)
    cbar.set_label("Coverage %", color=MUTED)

    ax.set_title(title, color=TEXT_COLOR, fontsize=11, pad=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=FIG_DPI, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print(f"  Saved {output_path.name}")


def plot_intent_heatmap(skills_data: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Intent coverage heatmap: skills × languages.

    Args:
        skills_data: Per-skill coverage dict.
        lang_order: Language codes in column order.
        plots_dir: Output directory for plots.
    """
    matrix, labels = _pct_matrix(skills_data, lang_order, "intent", top_n=60)
    _heatmap(matrix, labels, lang_order, "Intent File Coverage by Skill & Language",
             plots_dir / "intent_coverage_heatmap.png")


def plot_dialog_heatmap(skills_data: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Dialog coverage heatmap: skills × languages.

    Args:
        skills_data: Per-skill coverage dict.
        lang_order: Language codes in column order.
        plots_dir: Output directory for plots.
    """
    matrix, labels = _pct_matrix(skills_data, lang_order, "dialog", top_n=60)
    _heatmap(matrix, labels, lang_order, "Dialog File Coverage by Skill & Language",
             plots_dir / "dialog_coverage_heatmap.png")


def plot_coverage_by_language(summary: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Grouped horizontal bar chart: intent / dialog / voc coverage per language.

    Args:
        summary: Summary section from coverage_data.json.
        lang_order: Language codes to include (English skipped).
        plots_dir: Output directory for plots.
    """
    lang_stats = summary["languages"]
    # Sort by combined_pct descending
    sorted_langs = sorted(
        [l for l in lang_order if l != "en"],
        key=lambda l: lang_stats.get(l, {}).get("combined_pct", 0),
        reverse=True,
    )

    intent_pcts = [lang_stats.get(l, {}).get("intent_pct", 0) for l in sorted_langs]
    dialog_pcts = [lang_stats.get(l, {}).get("dialog_pct", 0) for l in sorted_langs]
    voc_pcts = [lang_stats.get(l, {}).get("voc_pct", 0) for l in sorted_langs]

    y = np.arange(len(sorted_langs))
    bar_h = 0.22

    fig, ax = plt.subplots(figsize=(10, max(4, len(sorted_langs) * 0.5 + 1.5)))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)

    ax.barh(y + bar_h, intent_pcts, bar_h, color=ACCENT, label="Intent", alpha=0.9)
    ax.barh(y, dialog_pcts, bar_h, color="#3b82f6", label="Dialog", alpha=0.9)
    ax.barh(y - bar_h, voc_pcts, bar_h, color="#a855f7", label="Vocab/Entity", alpha=0.9)

    ax.set_yticks(y)
    ax.set_yticklabels(sorted_langs, fontsize=10)
    ax.set_xlabel("Coverage %", color=MUTED)
    ax.set_xlim(0, 105)
    ax.axvline(100, color=BORDER, linewidth=0.8, linestyle="--")
    ax.grid(axis="x")

    # Annotate values
    for i, (ip, dp, vp) in enumerate(zip(intent_pcts, dialog_pcts, voc_pcts)):
        if ip > 3:
            ax.text(ip + 0.5, i + bar_h, f"{ip:.0f}%", va="center", fontsize=7, color=TEXT_COLOR)
        if dp > 3:
            ax.text(dp + 0.5, i, f"{dp:.0f}%", va="center", fontsize=7, color=TEXT_COLOR)
        if vp > 3:
            ax.text(vp + 0.5, i - bar_h, f"{vp:.0f}%", va="center", fontsize=7, color=TEXT_COLOR)

    ax.legend(loc="lower right", facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_COLOR)
    ax.set_title("Locale Coverage by Language and File Type", color=TEXT_COLOR, fontsize=11, pad=10)
    plt.tight_layout()
    plt.savefig(plots_dir / "coverage_by_language.png", dpi=FIG_DPI, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("  Saved coverage_by_language.png")


def plot_combined_heatmap(skills_data: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Combined (intent+dialog) coverage heatmap for the 40 most complex skills.

    Args:
        skills_data: Per-skill coverage dict.
        lang_order: Language codes in column order.
        plots_dir: Output directory for plots.
    """
    rows = []
    labels = []
    for skill_id, skill in skills_data.items():
        t_intent = skill["totals"].get("intent", 0)
        t_dialog = skill["totals"].get("dialog", 0)
        t_total = t_intent + t_dialog
        if t_total == 0:
            continue
        row = []
        for lang in lang_order:
            c_intent = skill["languages"].get(lang, {}).get("intent", 0)
            c_dialog = skill["languages"].get(lang, {}).get("dialog", 0)
            row.append(round((c_intent + c_dialog) / t_total * 100, 1))
        rows.append((t_total, row,
                     skill["display_name"].replace("ovos-skill-", "").replace("ovos-", "")))

    # Sort by complexity (total files) descending, take top 40
    rows.sort(key=lambda x: x[0], reverse=True)
    rows = rows[:40]
    matrix = np.array([r[1] for r in rows])
    labels = [r[2] for r in rows]

    _heatmap(matrix, labels, lang_order,
             "Combined Intent+Dialog Coverage (Top 40 Skills by Complexity)",
             plots_dir / "combined_heatmap.png")


def plot_intent_vs_dialog_gap(skills_data: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Scatter plot: intent coverage % vs dialog coverage % per skill, coloured by language.

    Skills in the bottom-right quadrant have high intent but low dialog coverage.

    Args:
        skills_data: Per-skill coverage dict.
        lang_order: Language codes in column order.
        plots_dir: Output directory for plots.
    """
    # Pick a subset of languages to avoid overplotting
    sample_langs = [l for l in lang_order if l not in ("en",)][:8]
    lang_colors = plt.cm.tab10(np.linspace(0, 1, len(sample_langs)))  # type: ignore[attr-defined]

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)

    for lang_idx, lang in enumerate(sample_langs):
        xs, ys, sizes = [], [], []
        for skill in skills_data.values():
            t_intent = skill["totals"].get("intent", 0)
            t_dialog = skill["totals"].get("dialog", 0)
            if t_intent == 0 or t_dialog == 0:
                continue
            c_intent = skill["languages"].get(lang, {}).get("intent", 0)
            c_dialog = skill["languages"].get(lang, {}).get("dialog", 0)
            xs.append(c_intent / t_intent * 100)
            ys.append(c_dialog / t_dialog * 100)
            sizes.append(max(20, (t_intent + t_dialog) * 2))

        ax.scatter(xs, ys, s=sizes, alpha=0.55, color=lang_colors[lang_idx],
                   label=lang, edgecolors="none")

    # Diagonal reference line (intent == dialog)
    ax.plot([0, 100], [0, 100], color=BORDER, linewidth=1, linestyle="--", zorder=0)

    ax.set_xlabel("Intent Coverage %", color=MUTED)
    ax.set_ylabel("Dialog Coverage %", color=MUTED)
    ax.set_xlim(-2, 105)
    ax.set_ylim(-2, 105)
    ax.grid(True)
    ax.legend(facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_COLOR, fontsize=8)
    ax.set_title(
        "Intent vs Dialog Coverage Gap\n(bottom-right = intent translated but dialog missing)",
        color=TEXT_COLOR, fontsize=10, pad=10,
    )

    # Shade gap quadrant
    ax.fill_between([50, 105], [0, 0], [50, 50], alpha=0.05, color="#ef4444",
                    label="_nolegend_")
    ax.text(77, 10, "gap zone", color="#ef4444", fontsize=8, alpha=0.7)

    plt.tight_layout()
    plt.savefig(plots_dir / "intent_vs_dialog_gap.png", dpi=FIG_DPI, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("  Saved intent_vs_dialog_gap.png")


def generate_plots(output_dir: Path | None = None) -> None:
    """Read coverage_data.json and generate all 5 plots.

    Args:
        output_dir: Directory containing coverage_data.json and plots/ subdir.
                    Defaults to the directory containing this script.
    """
    if output_dir is None:
        output_dir = Path(__file__).parent

    coverage_path = output_dir / "coverage_data.json"
    if not coverage_path.exists():
        print(f"ERROR: {coverage_path} not found. Run compute_coverage.py first.")
        return

    with open(coverage_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills_data = data["skills"]
    summary = data["summary"]
    lang_order: list[str] = data.get("tracked_languages", [])

    plots_dir = output_dir / PLOTS_DIR_NAME
    plots_dir.mkdir(exist_ok=True)

    _apply_dark_theme()

    print("Generating plots...")
    plot_intent_heatmap(skills_data, lang_order, plots_dir)
    plot_dialog_heatmap(skills_data, lang_order, plots_dir)
    plot_coverage_by_language(summary, lang_order, plots_dir)
    plot_combined_heatmap(skills_data, lang_order, plots_dir)
    plot_intent_vs_dialog_gap(skills_data, lang_order, plots_dir)
    print(f"All plots saved to {plots_dir}/")


if __name__ == "__main__":
    generate_plots()
