import os

CSV = []
for fname in os.listdir(os.path.dirname(__file__)):
    if not fname.endswith(".csv") or not fname.startswith("intents_"):
        continue
    lang = fname.split("_")[-1].split(".csv")[0]
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as f:
        for line in f.read().split("\n")[1:]:
            if not line.strip():
                continue
            domain, intent, utterance = line.split(",", 2)
            CSV.append(f"{lang}\t{domain}\t{intent}\t{utterance}")

CSV = sorted(set(CSV))
CSV.insert(0, "lang\tdomain\tintent\tutterance")
print(len(CSV) - 1, "dataset entries")

with open("gitlocalize_dataset.tsv", "w") as f:
    f.write("\n".join(CSV))