this repo provides config snippets for OVOS

there are 4 folders, each containing a config file optimized for each language

this includes default plugins and other settings such as units and date format

```
.
├── offline_female
│   ├── ca-es.conf
│   ├── de-de.conf
│   ├── en-gb.conf
│   ├── en-us.conf
│   ├── es-es.conf
│   ├── fr-fr.conf
│   ├── gl-es.conf
│   ├── it-it.conf
│   └── nl-nl.conf
├── offline_male
│   ├── ca-es.conf
│   ├── de-de.conf
│   ├── en-gb.conf
│   ├── en-us.conf
│   ├── es-es.conf
│   ├── fr-fr.conf
│   ├── gl-es.conf
│   ├── it-it.conf
│   ├── nl-nl.conf
│   ├── pt-br.conf
│   └── pt-pt.conf
├── online_female
│   ├── ca-ba.conf
│   ├── ca-es.conf
│   ├── ca-nw.conf
│   ├── ca-va.conf
│   ├── de-de.conf
│   ├── en-gb.conf
│   ├── en-us.conf
│   ├── es-es.conf
│   ├── fr-fr.conf
│   ├── it-it.conf
│   └── nl-nl.conf
└── online_male
    ├── ca-ba.conf
    ├── ca-es.conf
    ├── ca-nw.conf
    ├── ca-va.conf
    ├── de-de.conf
    ├── en-gb.conf
    ├── en-us.conf
    ├── es-es.conf
    ├── fr-fr.conf
    ├── it-it.conf
    ├── nl-nl.conf
    ├── pt-br.conf
    └── pt-pt.conf

```

PRs welcome!

## STT Comparison

> self reported WER score from model pages, **not independently verified**

#### Spanish

| Plugin                        | Model                                         | CV12  | CV13    |
|-------------------------------|-----------------------------------------------|-------|---------|
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-es`                   |       | 4.8949  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-es`                      |       | 5.1265  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-es`                     |       | 5.4088  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-es`                      |       | 8.2668  |
| ovos-stt-plugin-citrinet      | `neongeckocom/stt_es_citrinet_512_gamma_0_25` | 9.549 |         |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-es`                       |       | 13.5312 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-es`                       |       | 19.5904 |

#### Catalan

| Plugin                        | Model                                         | CV11  | CV12  | CV13    | CV17 (test) | CV17 (dev) | 3CatParla (test) | 3CatParla (dev) |
|-------------------------------|-----------------------------------------------|-------|-------|---------|-------------|------------|------------------|-----------------|
| ovos-stt-plugin-fasterwhisper | `projecte-aina/whisper-large-v3-ca-3catparla` |       |       |         | 10.320      | 9.260      | 0.960            | 0.920           |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-ca`                   |       |       | 4.6716  |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-ca`                      |       |       | 5.0700  |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v3-ca`                   |       |       | 5.9714  |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-ca`                     |       |       | 5.9954  |             |            |                  |                 |
| ovos-stt-plugin-citrinet      | `projecte-aina/stt-ca-citrinet-512`           | 6.684 |       |         |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-ca`                      |       |       | 10.0252 |             |            |                  |                 |
| ovos-stt-plugin-citrinet      | `neongeckocom/stt_ca_citrinet_512_gamma_0_25` |       | 8.065 |         |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-ca`                       |       |       | 13.7897 |             |            |                  |                 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-ca`                       |       |       | 16.9043 |             |            |                  |                 |

#### Galician

| Plugin                        | Model                       | CV13    |
|-------------------------------|-----------------------------|---------|
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-gl` | 5.9879  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-gl`    | 6.9398  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-gl`   | 7.1227  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-gl`    | 10.9875 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-gl`     | 18.6879 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-gl`     | 26.3504 |

#### Basque

| Plugin                        | Model                              | CV13    |
|-------------------------------|------------------------------------|---------|
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v3-eu-cv16_1` | 6.8880  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-eu-cv16_1` | 7.7204  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-eu-cv16_1`    | 8.1444  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-eu-cv16_1`   | 9.2006  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-eu-cv16_1`    | 12.7374 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-eu-cv16_1`     | 16.1765 |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-eu-cv16_1`     | 19.0949 |

#### Portuguese

| Plugin                        | Model                                         | CV12  | CV13   | Fleurs |
|-------------------------------|-----------------------------------------------|-------|--------|--------|
| ovos-stt-plugin-fasterwhisper | `my-north-ai/whisper-large-v3-pt`             |       |        | 4.65   |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v3-pt`                   |       | 4.6003 |        |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-pt`                   |       | 5.875  |        |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-pt`                      |       | 6.399  |        |
| ovos-stt-plugin-fasterwhisper | `my-north-ai/whisper-medium`                  |       |        | 6.57   |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-pt`                     |       | 6.332  |        |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-pt`                      |       | 10.252 |        |
| ovos-stt-plugin-citrinet      | `neongeckocom/stt_pt_citrinet_512_gamma_0_25` | 6.033 |        |        |
| ovos-stt-plugin-fasterwhisper | `my-north-ai/whisper-small`                   |       |        | 10.34  |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-pt`                       |       | 19.290 |        |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-pt`                       |       | 28.965 |        |

#### English

| Plugin                   | Model                                         | LibriSpeech (clean) |  
|--------------------------|-----------------------------------------------|---------------------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_en_citrinet_512_gamma_0_25` | 3.400               | 

#### French

| Plugin                   | Model                                         | CV12   |  
|--------------------------|-----------------------------------------------|--------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_fr_citrinet_512_gamma_0_25` | 14.900 | 

#### German

| Plugin                   | Model                                         | CV12   |  
|--------------------------|-----------------------------------------------|--------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_de_citrinet_512_gamma_0_25` | 11.100 | 

#### Italian

| Plugin                   | Model                                         | CV12  |  
|--------------------------|-----------------------------------------------|-------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_it_citrinet_512_gamma_0_25` | 9.232 | 

#### Ukrainian

| Plugin                   | Model                                         | CV10  |  
|--------------------------|-----------------------------------------------|-------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_uk_citrinet_512_gamma_0_25` | 8.609 | 

#### Dutch

| Plugin                   | Model                                         | CV12  |  
|--------------------------|-----------------------------------------------|-------| 
| ovos-stt-plugin-citrinet | `neongeckocom/stt_nl_citrinet_512_gamma_0_25` | 6.204 | 

## Info Maps

Date format per country

![img_1.png](img_1.png)

System units per country

![img.png](img.png)