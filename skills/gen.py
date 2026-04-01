#!/usr/bin/env python
"""
Skill Documentation and Dataset Generator.

This script parses installed OVOS (Open Voice OS) skill plugins to generate
markdown documentation and formatted CSV datasets (intents and utterances)
for multiple languages.
"""

import csv
import importlib
import json
import os

from langcodes import closest_supported_match
from ovos_plugin_manager.skills import find_skill_plugins
from ovos_utils.bracket_expansion import expand_template


def generate_skill_data(languages: list = None, output_dir: str = None) -> None:
    """
    Generate markdown documentation and sorted CSV datasets for OVOS skills.

    Args:
        languages (list, optional): List of language codes to process. Defaults to
                                    a predefined list of supported languages.
        output_dir (str, optional): Directory to save the output files. Defaults to
                                    the directory of this script.
    """
    if languages is None:
        languages = ["ca", "de", "en", "pt", "fr", "it", "da", "gl", "eu", "es", "nl"]

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # Fetch plugins
    plugins = find_skill_plugins()
    if not plugins:
        print("No skill plugins found. Exiting.")
        return

    sorted_skills = sorted(plugins.keys())

    for lang in languages:
        md_path = os.path.join(output_dir, f"skills_{lang}.md")

        # Use lists to accumulate data so we can sort them easily later
        intents_data = []
        dialogs_data = []
        utterances_data = []

        with open(md_path, "w", encoding="utf-8") as md_file:
            for skill_id in sorted_skills:
                plug = plugins[skill_id]
                plugin_module = importlib.import_module(plug.__module__)
                base_locale_dir = os.path.join(os.path.dirname(plugin_module.__file__), "locale")

                if not os.path.isdir(base_locale_dir):
                    continue

                locale = closest_supported_match(lang, os.listdir(base_locale_dir))
                if locale is None or locale == "und":
                    continue

                locale_dir = os.path.join(base_locale_dir, locale)
                for root, _, files in os.walk(locale_dir):

                    # 1. Process Intent Files
                    intent_files = [f for f in files if f.endswith(".intent")]
                    for intent_filename in intent_files:
                        intent_path = os.path.join(root, intent_filename)

                        with open(intent_path, "r", encoding="utf-8") as ifile:
                            lines = ifile.read().splitlines()

                        for line in lines:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue

                            # Expand bracket templates and add to intents list
                            for expanded_line in expand_template(line):
                                if expanded_line:
                                    intents_data.append((skill_id, intent_filename, expanded_line))

                    # 2. Process Dialog Files (first valid line per file = the combo)
                    dialog_files = [f for f in files if f.endswith(".dialog")]
                    for dialog_filename in dialog_files:
                        dialog_path = os.path.join(root, dialog_filename)
                        with open(dialog_path, "r", encoding="utf-8") as dfile:
                            lines = dfile.read().splitlines()
                        first_line = next(
                            (l.strip() for l in lines if l.strip() and not l.strip().startswith("#")),
                            None,
                        )
                        if first_line:
                            dialogs_data.append((skill_id, dialog_filename, first_line))

                    # 3. Process skill.json for Markdown and Examples CSV
                    if "skill.json" in files:
                        skill_json_path = os.path.join(root, "skill.json")
                        with open(skill_json_path, "r", encoding="utf-8") as fi:
                            data = json.load(fi)

                        # Filter out empty examples
                        examples = [e for e in data.get("examples", []) if e]
                        if not examples:
                            continue

                        examples.sort()

                        # Write to Markdown
                        md_file.write(f"\n### {skill_id.lower()}\n")
                        description = data.get('description', 'No description available')
                        md_file.write(f"\n{description}")
                        md_file.write(f"\n\n**Usage examples:**")

                        # Write up to 10 examples to Markdown and accumulate them for CSV
                        for example in examples[:10]:
                            md_file.write(f"\n- {example}")
                            utterances_data.append((skill_id, example))

                        md_file.write("\n\n-------\n\n")

        # Sort the accumulated data to ensure clean git diffs
        intents_data.sort()
        dialogs_data.sort()
        utterances_data.sort()

        # Write Intents CSV
        intents_csv_path = os.path.join(output_dir, f"intents_{lang}.csv")
        with open(intents_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["domain", "intent", "utterance"])
            writer.writerows(intents_data)

        # Write Dialogs CSV (one row per dialog file, first valid line only)
        dialogs_csv_path = os.path.join(output_dir, f"dialogs_{lang}.csv")
        with open(dialogs_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["domain", "dialog", "line"])
            writer.writerows(dialogs_data)

        # Write Utterances CSV
        utterances_csv_path = os.path.join(output_dir, f"utterances_{lang}.csv")
        with open(utterances_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["domain", "utterance"])
            writer.writerows(utterances_data)


if __name__ == "__main__":
    generate_skill_data()