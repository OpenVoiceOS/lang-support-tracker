import os


def json_to_markdown_table(json_data):
    # Define the table header
    key2header = ['system_unit', 'date_format',
                  'online_stt', 'offline_stt',
                  'online_tts', 'online_tts_male', 'online_tts_female',
                  'offline_tts', 'offline_tts_male', 'offline_tts_female']

    table_clean = ["Lang"] + [w.replace("_", " ").title().replace("Stt", "STT").replace("Tts", "TTS")
                              for w in key2header]

    # Create the table header row in Markdown format
    md_table = f"| {' | '.join(table_clean)} |\n"
    md_table += f"| {' | '.join(['---'] * len(table_clean))} |\n"

    for lang in sorted(json_data.keys()):
        row = [lang]
        for k in key2header:
            # Iterate through each item in the JSON and add rows to the Markdown table
            row.append(json_data[lang].get(k, "N/A"))
        md_table += f"| {' | '.join(row)} |\n"

    return md_table


def read_json_files_from_directory(directory_path):
    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".conf"):
            file_path = os.path.join(directory_path, filename)

            # Read the JSON file and load the data
            from ovos_config import LocalConf
            cfg = LocalConf(file_path)
            yield filename.split(".conf")[0], cfg


def save_markdown_table(md_table, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_table)


online_male_directory = os.path.dirname(__file__) + "/online_male"
online_female_directory = os.path.dirname(__file__) + "/online_female"
offline_male_directory = os.path.dirname(__file__) + "/offline_male"
offline_female_directory = os.path.dirname(__file__) + "/offline_female"

lang_data = {}

for lang, cfg in read_json_files_from_directory(online_male_directory):
    tts_plugin = cfg.get("tts", {}).get("module")
    if lang not in lang_data:
        lang_data[lang] = {
            "system_unit": cfg.get("system_unit"),
            "date_format": cfg.get("date_format")
        }
    lang_data[lang]["online_stt"] = cfg.get("stt", {}).get("module")
    lang_data[lang]["online_tts"] = tts_plugin
    lang_data[lang]["online_tts_male"] = cfg.get("tts", {}).get(tts_plugin, {}).get("voice")

for lang, cfg in read_json_files_from_directory(offline_male_directory):
    tts_plugin = cfg.get("tts", {}).get("module")
    if lang not in lang_data:
        lang_data[lang] = {
            "system_unit": cfg.get("system_unit"),
            "date_format": cfg.get("date_format")
        }
    lang_data[lang]["offline_stt"] = cfg.get("stt", {}).get("module")
    lang_data[lang]["offline_tts"] = tts_plugin
    lang_data[lang]["offline_tts_male"] = cfg.get("tts", {}).get(tts_plugin, {}).get("voice")

for lang, cfg in read_json_files_from_directory(online_female_directory):
    tts_plugin = cfg.get("tts", {}).get("module")
    if lang not in lang_data:
        lang_data[lang] = {
            "system_unit": cfg.get("system_unit"),
            "date_format": cfg.get("date_format")
        }
    lang_data[lang]["online_tts"] = tts_plugin
    lang_data[lang]["online_tts_female"] = cfg.get("tts", {}).get(tts_plugin, {}).get("voice")

for lang, cfg in read_json_files_from_directory(offline_female_directory):
    tts_plugin = cfg.get("tts", {}).get("module")
    if lang not in lang_data:
        lang_data[lang] = {
            "system_unit": cfg.get("system_unit"),
            "date_format": cfg.get("date_format")
        }
    lang_data[lang]["offline_tts"] = tts_plugin
    lang_data[lang]["offline_tts_female"] = cfg.get("tts", {}).get(tts_plugin, {}).get("voice")

markdown = json_to_markdown_table(lang_data)
print(markdown)
save_markdown_table(markdown, os.path.dirname(__file__) + "/cfg_report.md")