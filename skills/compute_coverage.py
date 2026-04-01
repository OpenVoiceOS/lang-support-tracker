#!/usr/bin/env python
"""
Skill locale coverage calculator.

Walks all installed OVOS skill plugins and computes per-skill, per-language,
per-filetype coverage. Coverage is binary: a file is "covered" if it exists
in the target language locale and contains at least one non-empty,
non-comment line. This reflects that .intent/.dialog files need only 1
translated line to be functional.

Output: skills/coverage_data.json
"""

import json
import os
import importlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from langcodes import closest_supported_match
from ovos_plugin_manager.skills import find_skill_plugins


# File types to track coverage for
FILE_TYPES: list[str] = [".intent", ".dialog", ".voc", ".entity"]

# Languages to track (short codes used by gen.py)
LANGUAGES: list[str] = ["ca", "da", "de", "es", "eu", "fr", "gl", "it", "nl", "pt"]

# Preferred source locale (used as first candidate)
SOURCE_LANG: str = "en"


def has_valid_content(file_path: Path) -> bool:
    """Return True if file has at least one non-empty, non-comment line.

    Args:
        file_path: Path to the locale file.

    Returns:
        True if the file has usable content, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    return True
    except OSError:
        return False
    return False


def enumerate_locale_files(locale_dir: Path, filetypes: list[str]) -> dict[str, list[str]]:
    """Enumerate all files of given types under a locale directory.

    Returns a dict mapping each filetype to a sorted list of relative
    file paths (relative to locale_dir), preserving subdirectory structure
    so cross-language comparisons are path-consistent.

    Args:
        locale_dir: Root of the locale directory to scan.
        filetypes: List of file extensions to include (e.g. [".intent", ".dialog"]).

    Returns:
        Dict mapping filetype → list of relative paths (e.g. "dialog/weather.dialog").
    """
    result: dict[str, list[str]] = {ft: [] for ft in filetypes}
    if not locale_dir.is_dir():
        return result
    for root, _, files in os.walk(locale_dir):
        for fname in files:
            ext = Path(fname).suffix.lower()
            if ext in filetypes:
                rel_path = os.path.relpath(os.path.join(root, fname), locale_dir)
                result[ext].append(rel_path)
    for ft in result:
        result[ft].sort()
    return result


def count_covered_files(
    source_files: dict[str, list[str]],
    target_locale_dir: Path,
) -> dict[str, int]:
    """Count how many source files have valid translated counterparts.

    For each file in source_files, check whether the corresponding path
    exists under target_locale_dir and has valid content.

    Args:
        source_files: Dict mapping filetype → list of relative paths from source locale.
        target_locale_dir: Root of the target language locale directory.

    Returns:
        Dict mapping filetype → count of covered files.
    """
    covered: dict[str, int] = {}
    for ft, rel_paths in source_files.items():
        count = 0
        for rel_path in rel_paths:
            target_path = target_locale_dir / rel_path
            if target_path.exists() and has_valid_content(target_path):
                count += 1
        covered[ft] = count
    return covered


def find_locale_dir(base_locale_dir: Path, lang: str) -> Optional[Path]:
    """Resolve closest matching locale directory for a language code.

    Args:
        base_locale_dir: Base locale directory containing language subdirectories.
        lang: Language code to match (e.g. "ca", "de").

    Returns:
        Path to the matched locale directory, or None if not found.
    """
    if not base_locale_dir.is_dir():
        return None
    available = os.listdir(base_locale_dir)
    matched = closest_supported_match(lang, available)
    if matched is None or matched == "und":
        return None
    return base_locale_dir / matched


def find_source_locale_dir(base_locale_dir: Path) -> Optional[tuple[Path, str]]:
    """Determine the source (reference) locale for a skill.

    Prefers English if present. If the skill has no English locale at all,
    falls back to the locale with the highest file count across tracked types —
    this handles skills whose primary language is not English (e.g. a Catalan-
    first skill like ovos-skill-fuster-quotes).

    Args:
        base_locale_dir: Base locale directory containing language subdirectories.

    Returns:
        Tuple of (locale_path, lang_code) for the chosen source locale, or None.
    """
    if not base_locale_dir.is_dir():
        return None

    # Try English first
    en_dir = find_locale_dir(base_locale_dir, SOURCE_LANG)
    if en_dir is not None:
        en_files = enumerate_locale_files(en_dir, FILE_TYPES)
        if any(len(v) > 0 for v in en_files.values()):
            return en_dir, SOURCE_LANG

    # Fall back to the richest locale (most tracked files total)
    best_path: Optional[Path] = None
    best_count = 0
    best_lang = ""
    for entry in sorted(os.listdir(base_locale_dir)):
        candidate = base_locale_dir / entry
        if not candidate.is_dir():
            continue
        files = enumerate_locale_files(candidate, FILE_TYPES)
        count = sum(len(v) for v in files.values())
        if count > best_count:
            best_count = count
            best_path = candidate
            best_lang = entry
    if best_path is None or best_count == 0:
        return None
    return best_path, best_lang


def compute_coverage(output_dir: Optional[Path] = None) -> dict:
    """Compute full per-skill, per-language, per-filetype coverage matrix.

    Args:
        output_dir: Directory to write coverage_data.json. Defaults to the
                    directory containing this script.

    Returns:
        The full coverage data dict (also written to coverage_data.json).
    """
    if output_dir is None:
        output_dir = Path(__file__).parent

    plugins = find_skill_plugins()
    if not plugins:
        print("No skill plugins found. Exiting.")
        return {}

    skills_data: dict = {}

    for skill_id in sorted(plugins.keys()):
        plug = plugins[skill_id]
        try:
            plugin_module = importlib.import_module(plug.__module__)
        except Exception:
            continue
        base_locale_dir = Path(os.path.dirname(plugin_module.__file__)) / "locale"

        # Resolve source locale (English preferred; fallback to richest locale)
        source_result = find_source_locale_dir(Path(base_locale_dir))
        if source_result is None:
            continue
        source_locale_dir, source_lang_code = source_result

        # Enumerate source files
        source_files = enumerate_locale_files(source_locale_dir, FILE_TYPES)
        totals = {ft.lstrip("."): len(paths) for ft, paths in source_files.items()}

        # Skip skills with no locale files of any tracked type
        if all(v == 0 for v in totals.values()):
            continue

        lang_coverage: dict[str, dict[str, int]] = {}

        # Source locale = 100% by definition (stored under "en" key for dashboard compat)
        lang_coverage["en"] = {ft.lstrip("."): len(paths) for ft, paths in source_files.items()}

        # Process each target language
        for lang in LANGUAGES:
            target_locale_dir = find_locale_dir(base_locale_dir, lang)
            if target_locale_dir is None:
                lang_coverage[lang] = {ft.lstrip("."): 0 for ft in FILE_TYPES}
                continue
            covered = count_covered_files(source_files, target_locale_dir)
            lang_coverage[lang] = {ft.lstrip("."): cnt for ft, cnt in covered.items()}

        display_name = skill_id.split(".")[0]  # strip .openvoiceos suffix

        skills_data[skill_id] = {
            "display_name": display_name,
            "source_lang": source_lang_code,
            "totals": totals,
            "languages": lang_coverage,
        }

    # Build summary
    summary = _build_summary(skills_data)

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_lang": SOURCE_LANG,
        "file_types": [ft.lstrip(".") for ft in FILE_TYPES],
        "tracked_languages": LANGUAGES,
        "summary": summary,
        "skills": skills_data,
    }

    output_path = output_dir / "coverage_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Coverage data written to {output_path}")
    print(f"  Skills tracked: {summary['total_skills']}")
    for lang, stats in summary["languages"].items():
        print(
            f"  {lang:6s}  intent={stats['intent_pct']:5.1f}%  "
            f"dialog={stats['dialog_pct']:5.1f}%  "
            f"voc={stats['voc_pct']:5.1f}%  "
            f"combined={stats['combined_pct']:5.1f}%"
        )
    return output


def _build_summary(skills_data: dict) -> dict:
    """Aggregate per-skill coverage into language-level summary statistics.

    Args:
        skills_data: Per-skill coverage dict as built by compute_coverage().

    Returns:
        Summary dict with totals and per-language aggregated metrics.
    """
    # Global totals from English source
    total_skills = len(skills_data)
    global_totals: dict[str, int] = {ft.lstrip("."): 0 for ft in FILE_TYPES}
    for skill in skills_data.values():
        for ft, count in skill["totals"].items():
            global_totals[ft] = global_totals.get(ft, 0) + count

    lang_summaries: dict[str, dict] = {}
    all_langs = ["en"] + LANGUAGES

    for lang in all_langs:
        covered_totals: dict[str, int] = {ft.lstrip("."): 0 for ft in FILE_TYPES}
        skills_with_any = 0
        skills_full_intent = 0

        for skill in skills_data.values():
            lang_data = skill["languages"].get(lang, {})
            has_any = False
            for ft in covered_totals:
                c = lang_data.get(ft, 0)
                covered_totals[ft] += c
                if c > 0:
                    has_any = True
            if has_any:
                skills_with_any += 1
            if lang_data.get("intent", 0) >= skill["totals"].get("intent", 0) > 0:
                skills_full_intent += 1

        def pct(covered: int, total: int) -> float:
            return round(covered / total * 100, 1) if total > 0 else 0.0

        # Combined = weighted across intent + dialog + voc files
        combined_covered = (
            covered_totals.get("intent", 0)
            + covered_totals.get("dialog", 0)
            + covered_totals.get("voc", 0)
        )
        combined_total = (
            global_totals.get("intent", 0)
            + global_totals.get("dialog", 0)
            + global_totals.get("voc", 0)
        )

        lang_summaries[lang] = {
            "skills_any_coverage": skills_with_any,
            "skills_full_intent": skills_full_intent,
            "intent_covered": covered_totals.get("intent", 0),
            "intent_total": global_totals.get("intent", 0),
            "intent_pct": pct(covered_totals.get("intent", 0), global_totals.get("intent", 0)),
            "dialog_covered": covered_totals.get("dialog", 0),
            "dialog_total": global_totals.get("dialog", 0),
            "dialog_pct": pct(covered_totals.get("dialog", 0), global_totals.get("dialog", 0)),
            "voc_covered": covered_totals.get("voc", 0),
            "voc_total": global_totals.get("voc", 0),
            "voc_pct": pct(covered_totals.get("voc", 0), global_totals.get("voc", 0)),
            "entity_covered": covered_totals.get("entity", 0),
            "entity_total": global_totals.get("entity", 0),
            "entity_pct": pct(covered_totals.get("entity", 0), global_totals.get("entity", 0)),
            "combined_covered": combined_covered,
            "combined_total": combined_total,
            "combined_pct": pct(combined_covered, combined_total),
        }

    return {
        "total_skills": total_skills,
        "total_intent_files": global_totals.get("intent", 0),
        "total_dialog_files": global_totals.get("dialog", 0),
        "total_voc_files": global_totals.get("voc", 0),
        "total_entity_files": global_totals.get("entity", 0),
        "languages": lang_summaries,
    }


if __name__ == "__main__":
    compute_coverage()
