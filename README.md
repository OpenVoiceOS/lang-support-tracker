# OVOS Language Support Tracker

**Your help with translations is invaluable!**

> You can find us on [Gitlocalize](https://gitlocalize.com/users/OpenVoiceOS), a text and video translation tutorial is available at [https://www.openvoiceos.org/translation](https://www.openvoiceos.org/translation)

## Translations Status

translation status from our [Gitlocalize](https://gitlocalize.com/users/OpenVoiceOS) platform are available with detailed stats per repository. 

The table below lists languages that are at least 25% translated, note that these numbers may decrease whenever new strings become available for translation

____

| Lang | Translated % |
| --- | --- |
| da | 0.98 |
| de-DE | 0.97 |
| ca | 0.87 |
| gl | 0.86 |
| pt-PT | 0.65 |
| pt-BR | 0.54 |
| it-IT | 0.48 |
| es-ES | 0.43 |
| nl-NL | 0.4 |
| fr-FR | 0.38 |
| eu | 0.38 |


____

## 📢 **Language Support in OVOS Needs Your Help!**

Hey OVOS community! 🚀

If you’re using **raspOVOS** or any OVOS installation, we need **real-world data** to improve performance! 🫵

- 🟢 **[GitLocalize Benchmarks](https://gitlocalize-bench.tigregotico.pt/)** show between **70%** and **90%+ accuracy** depending on language
- 🔴 **User Reports** from the latest **raspOVOS images** indicate **high intent failure rates** in real use!

This gap shows why **training data alone isn’t enough**—we need **fresh test data** to:

- 🛠 Identify **intent failures** in daily usage
- 🗣 Spot **translation mistakes** affecting accuracy
- 📊 Improve **models & pipelines**

### **🌍 How to Help?**

1️⃣ **Enable Open Data Collection in raspOVOS (or your OVOS instance)**

- Add this to your `mycroft.conf`:

```json
"open_data": {
  "intent_urls": [
    "https://metrics.tigregotico.pt/intents"
  ]
}
```

_(Or self-host to track your own assistant’s failed intents! 🔧 [More info](https://github.com/OpenVoiceOS/ovos-opendata-server))_

2️⃣ **Monitor Progress & Data Collection:**

- 📊 **Live Dashboard:** [opendata.tigregotico.pt](https://opendata.tigregotico.pt/)
- ✅ **Server Status:** [metrics.tigregotico.pt/status](https://metrics.tigregotico.pt/status)


> OVOS is getting **more users**, but **without native speakers contributing real data, accuracy will suffer!**

Thanks for your help! Let’s make OVOS **great for every language** together! 🚀💙

____


## Open Data

benchmark explorers:

- [meteocat](https://meteocat.bench.tigregotico.pt) - catalan benchmark for weather queries
- [gitlocalize-bench](https://gitlocalize-bench.tigregotico.pt/) - padatious benchmark to evaluate gitlocalize intents
- [stt-bench](https://stt-bench.tigregotico.pt) - evaluating STT plugins against various datasets
- [tts-bench](https://tts-bench.tigregotico.pt) - evaluating TTS plugins
  
per language skill usage overview in markdown format:

- [skills_ca.md](skills/skills_ca.md)
- [skills_da.md](skills/skills_da.md)
- [skills_de.md](skills/skills_de.md)
- [skills_en.md](skills/skills_en.md)
- [skills_es.md](skills/skills_es.md)
- [skills_eu.md](skills/skills_eu.md)
- [skills_fr.md](skills/skills_fr.md)
- [skills_gl.md](skills/skills_gl.md)
- [skills_it.md](skills/skills_it.md)
- [skills_nl.md](skills/skills_nl.md)
- [skills_pt.md](skills/skills_pt.md)

csv exports of skill padatious intents:

- [intents_ca.csv](skills/intents_ca.csv)
- [intents_da.csv](skills/intents_da.csv)
- [intents_de.csv](skills/intents_de.csv)
- [intents_en.csv](skills/intents_en.csv)
- [intents_es.csv](skills/intents_es.csv)
- [intents_eu.csv](skills/intents_eu.csv)
- [intents_fr.csv](skills/intents_fr.csv)
- [intents_gl.csv](skills/intents_gl.csv)
- [intents_it.csv](skills/intents_it.csv)
- [intents_nl.csv](skills/intents_nl.csv)
- [intents_pt.csv](skills/intents_pt.csv)

json dumps for gitlocalize translation stats:

- [ca-ES.json](tx_info/ca.json)
- [da-DK.json](tx_info/da.json)
- [de-DE.json](tx_info/de-DE.json)
- [es-ES.json](tx_info/es-ES.json)
- [eu.json](tx_info/eu.json)
- [fr-FR.json](tx_info/fr-FR.json)
- [gl-ES.json](tx_info/gl.json)
- [it-IT.json](tx_info/it-IT.json)
- [nl-NL.json](tx_info/nl-NL.json)
- [pt-PT.json](tx_info/pt-PT.json)

per language translation overview in markdown format:

- [translate_status_ca.md](tx_info/translate_status_ca.md)
- [translate_status_da.md](tx_info/translate_status_da.md)
- [translate_status_de.md](tx_info/translate_status_de-DE.md)
- [translate_status_es.md](tx_info/translate_status_es-ES.md)
- [translate_status_eu.md](tx_info/translate_status_eu.md)
- [translate_status_fr.md](tx_info/translate_status_fr-FR.md)
- [translate_status_gl.md](tx_info/translate_status_gl.md)
- [translate_status_it.md](tx_info/translate_status_it-IT.md)
- [translate_status_nl.md](tx_info/translate_status_nl-NL.md)
- [translate_status_pt.md](tx_info/translate_status_pt-PT.md)

---

## Info Maps

Date format per country

![img_1.png](img_1.png)

System units per country

![img.png](img.png)

Temperature units per country

![img_3.png](img_3.png)

Clock format per country (12 vs 24h)

![img_2.png](img_2.png)

Numbering system per country

![image](https://github.com/user-attachments/assets/7cd69252-ff6f-4dc4-8d19-6627d87ecf73)

