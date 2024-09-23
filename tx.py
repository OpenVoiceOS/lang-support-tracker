import json
import os
import requests
import langcodes
from pprint import pprint
# i will adopt bs4 or selenium when it breaks, no dependencies is awesome ;)

EXPORT_PATH = f"{os.path.dirname(__file__)}/tx_info"
os.makedirs(EXPORT_PATH, exist_ok=True)

# get repos
URL = "https://gitlocalize.com/users/OpenVoiceOS"
r = requests.get(URL).text
repos = [l.split('href="/repo/')[-1].split('">')[0] for l in r.split("\n") if 'href="/repo/' in l]
skips = ["9661", "9660"]  # skip docs repos
repos =[r for r in repos if r not in skips]
per_lang = {}

# parse repos
for r in repos:
    repo_data = {}

    url = f"https://gitlocalize.com/repo/{r}"
    h = requests.get(url).text
    t = f'<a href="/repo/{r}/'

    title = h.split("<title>")[-1].split(" | GitLocalize")[0]
    links = [l.split('href="/repo/')[-1] for l in h.split("<tbody>")[-1].split("\n") if 'href="/repo/' in l]
    langs = [l.split('">')[0].split("/")[-1] for l in links if l.startswith(r)]

    tx_info = [l.strip() for l in h.split("\n") if "total-chars-data=" in l]
    for idx, data in enumerate(tx_info):
        lang = langs[idx]
        lang = langcodes.standardize_tag(lang, macro=True)
        # further normalize bad lang codes submitted
        # TODO - update as needed, or fix it GitLocalize side...
        if lang == "de":
            lang = "de-DE"
        if lang == "es":
            lang = "es-ES"
        if lang == "it":
            lang = "it-IT"

        if lang not in per_lang:
            per_lang[lang] = {}
        if r not in per_lang:
            per_lang[lang][r] = {"url": url, "title": title}
        info = {"url": url, "title": title}
        for s in data.split(" "):
            k, v = s.split("=")
            info[k] = v
        repo_data[lang] = info
        per_lang[lang][r] = info

    # uncomment if pre-repo is preferred
    #with open(f"{EXPORT_PATH}/{r}.json", "w") as f:
    #    json.dump(repo_data, f, indent=2)

# per lang summary
for lang, data in per_lang.items():
    with open(f"{EXPORT_PATH}/{lang}.json", "w") as f:
        json.dump(data, f, indent=2)
    # TODO - make a pretty markdown table

pprint(per_lang["ca"])
#