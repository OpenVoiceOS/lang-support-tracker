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

    # Sort by variance descending (most interesting gaps first), then by mean asc
    order = sorted(
        range(len(rows)),
        key=lambda i: (
            -float(np.std(rows[i])),  # high variance first
            float(np.mean(rows[i])),  # then by mean coverage asc
        ),
    )
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
    """Render and save a readable coverage heatmap.

    Uses a 4-tier categorical color scheme so the eye can quickly distinguish
    missing (0%), partial (<50%), good (50–99%), and full (100%) coverage.
    Cell annotations show the exact % value in every cell.

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

    # Tier colours: 0% = dark slate, <50% = muted red, <100% = amber, 100% = green
    TIER_NONE = "#1c1c1f"
    TIER_LOW = "#7f1d1d"
    TIER_MED = "#78350f"
    TIER_HIGH = "#14532d"
    TIER_FULL = "#15803d"

    def cell_color(v: float) -> str:
        if v == 0:
            return TIER_NONE
        if v < 50:
            return TIER_LOW
        if v < 100:
            return TIER_MED
        return TIER_FULL

    cell_height = 0.42
    cell_width = 1.1
    fig_height = max(5, n_rows * cell_height + 2.5)
    fig_width = max(7, n_cols * cell_width + 2.5)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    for r in range(n_rows):
        for c in range(n_cols):
            val = matrix[r, c]
            color = cell_color(val)
            rect = plt.Rectangle(  # type: ignore[attr-defined]
                (c - 0.5, r - 0.5), 1, 1,
                facecolor=color, edgecolor="#27272a", linewidth=0.4,
            )
            ax.add_patch(rect)
            # Text: white for dark cells, dark for bright cells
            txt_color = "#fafafa" if val < 100 else "#0a0a0b"
            label = "—" if val == 0 else f"{val:.0f}%"
            ax.text(c, r, label, ha="center", va="center",
                    fontsize=7.5, color=txt_color, fontweight="medium")

    ax.set_xlim(-0.5, n_cols - 0.5)
    ax.set_ylim(n_rows - 0.5, -0.5)  # flip: first skill at top
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(col_labels, fontsize=9, color=TEXT_COLOR)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=8, color=MUTED)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Legend
    legend_items = [
        mpatches.Patch(facecolor=TIER_FULL, edgecolor=BORDER, label="100%"),
        mpatches.Patch(facecolor=TIER_MED, edgecolor=BORDER, label="50–99%"),
        mpatches.Patch(facecolor=TIER_LOW, edgecolor=BORDER, label="1–49%"),
        mpatches.Patch(facecolor=TIER_NONE, edgecolor="#3f3f46", label="0%"),
    ]
    ax.legend(handles=legend_items, loc="lower right",
              facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_COLOR,
              fontsize=8, framealpha=0.9,
              bbox_to_anchor=(1.0, -0.04 - 0.8 / fig_height))

    ax.set_title(title, color=TEXT_COLOR, fontsize=11, pad=14, loc="left")
    plt.tight_layout(pad=1.0)
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


def plot_skills_per_language(skills_data: dict, summary: dict, lang_order: list[str], plots_dir: Path) -> None:
    """Per-language skill coverage breakdown: stacked bar showing full/partial/missing skills.

    Each bar shows how many skills have full intent coverage, partial intent,
    or no intent at all — giving a clear picture of skill completeness per language.

    Args:
        skills_data: Per-skill coverage dict.
        summary: Summary section from coverage_data.json.
        lang_order: Language codes to plot.
        plots_dir: Output directory for plots.
    """
    langs = [l for l in lang_order if l != "en"]

    full_intent = []
    partial_intent = []
    no_intent = []
    full_dialog = []
    partial_dialog = []
    no_dialog = []

    total_skills_with_intents = sum(
        1 for s in skills_data.values() if s["totals"].get("intent", 0) > 0
    )
    total_skills_with_dialogs = sum(
        1 for s in skills_data.values() if s["totals"].get("dialog", 0) > 0
    )

    for lang in langs:
        fi = pa = no = fd = pd_= nd = 0
        for skill in skills_data.values():
            t_i = skill["totals"].get("intent", 0)
            t_d = skill["totals"].get("dialog", 0)
            c_i = skill["languages"].get(lang, {}).get("intent", 0)
            c_d = skill["languages"].get(lang, {}).get("dialog", 0)
            if t_i > 0:
                if c_i == t_i:
                    fi += 1
                elif c_i > 0:
                    pa += 1
                else:
                    no += 1
            if t_d > 0:
                if c_d == t_d:
                    fd += 1
                elif c_d > 0:
                    pd_ += 1
                else:
                    nd += 1
        full_intent.append(fi)
        partial_intent.append(pa)
        no_intent.append(no)
        full_dialog.append(fd)
        partial_dialog.append(pd_)
        no_dialog.append(nd)

    # Sort langs by full_intent descending
    order = sorted(range(len(langs)), key=lambda i: full_intent[i] + partial_intent[i], reverse=True)
    langs = [langs[i] for i in order]
    full_intent = [full_intent[i] for i in order]
    partial_intent = [partial_intent[i] for i in order]
    no_intent = [no_intent[i] for i in order]
    full_dialog = [full_dialog[i] for i in order]
    partial_dialog = [partial_dialog[i] for i in order]
    no_dialog = [no_dialog[i] for i in order]

    x = np.arange(len(langs))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, max(4, len(langs) * 0.4 + 2)))
    fig.patch.set_facecolor(DARK_BG)
    for ax in (ax1, ax2):
        ax.set_facecolor(CARD_BG)

    # Intent panel
    b1 = ax1.bar(x, full_intent, width, label="Full coverage", color="#15803d", alpha=0.92)
    b2 = ax1.bar(x, partial_intent, width, bottom=full_intent,
                 label="Partial coverage", color="#78350f", alpha=0.92)
    b3 = ax1.bar(x, no_intent, width,
                 bottom=[f + p for f, p in zip(full_intent, partial_intent)],
                 label="No coverage", color="#1c1c1f", alpha=0.92)
    ax1.axhline(total_skills_with_intents, color=BORDER, linestyle="--", linewidth=0.8)
    ax1.text(len(langs) - 0.5, total_skills_with_intents + 0.3, f"total={total_skills_with_intents}",
             color=MUTED, fontsize=7.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(langs, fontsize=9, color=TEXT_COLOR)
    ax1.set_ylabel("Skills", color=MUTED)
    ax1.set_title("Intent Coverage per Language", color=TEXT_COLOR, fontsize=10, pad=8)
    ax1.legend(facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_COLOR, fontsize=8)

    # Dialog panel
    ax2.bar(x, full_dialog, width, label="Full coverage", color="#15803d", alpha=0.92)
    ax2.bar(x, partial_dialog, width, bottom=full_dialog,
            label="Partial coverage", color="#78350f", alpha=0.92)
    ax2.bar(x, no_dialog, width,
            bottom=[f + p for f, p in zip(full_dialog, partial_dialog)],
            label="No coverage", color="#1c1c1f", alpha=0.92)
    ax2.axhline(total_skills_with_dialogs, color=BORDER, linestyle="--", linewidth=0.8)
    ax2.text(len(langs) - 0.5, total_skills_with_dialogs + 0.3, f"total={total_skills_with_dialogs}",
             color=MUTED, fontsize=7.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(langs, fontsize=9, color=TEXT_COLOR)
    ax2.set_ylabel("Skills", color=MUTED)
    ax2.set_title("Dialog Coverage per Language", color=TEXT_COLOR, fontsize=10, pad=8)
    ax2.legend(facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_COLOR, fontsize=8)

    fig.suptitle("Skill Count by Coverage Status", color=TEXT_COLOR, fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig(plots_dir / "skills_per_language.png", dpi=FIG_DPI, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("  Saved skills_per_language.png")


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
    plot_skills_per_language(skills_data, summary, lang_order, plots_dir)
    print(f"All plots saved to {plots_dir}/")


if __name__ == "__main__":
    generate_plots()
