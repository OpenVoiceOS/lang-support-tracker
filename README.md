# OVOS Language Support Tracker

- [OVOS Language Support Tracker](#ovos-language-support-tracker)
  - [Recommended Configuration](#recommended-configuration)
  - [Voices Overview](#voices-overview)
  - [Translation Status](#translation-status)
  - [STT Comparison](#stt-comparison)
    - [Spanish](#spanish)
    - [Catalan](#catalan)
    - [Galician](#galician)
    - [Basque](#basque)
    - [Portuguese](#portuguese)
      
## Recommended Configuration

this repo provides config snippets for OVOS

there are 4 folders, each containing a config file optimized for each language

> These are meant only as reference and might not necessarily reflect the best config for your setup

These recommendations are meant to cover basic scenarios:
- `offline` - run everything locally, with acceptable latency in a modern computer
- `online` - use remote servers to offload compute, public or self hosted

| Lang | System Unit | Date Format | STT Servers | STT Plugin |
| --- | --- | --- | --- | --- |
| ca-ba | metric | DMY | - https://stt.smartgic.io/citrinet<br>- https://citrinetstt.ziggyai.online | N/A |
| ca-es | metric | DMY | - https://stt.smartgic.io/citrinet<br>- https://citrinetstt.ziggyai.online | [ovos-stt-plugin-citrinet](https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet) |
| ca-nw | metric | DMY | - https://stt.smartgic.io/citrinet<br>- https://citrinetstt.ziggyai.online | N/A |
| ca-va | metric | DMY | - https://stt.smartgic.io/citrinet<br>- https://citrinetstt.ziggyai.online | N/A |
| de-de | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-citrinet](https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet) |
| en-gb | english | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-fasterwhisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper) |
| en-us | english | MDY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-fasterwhisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper) |
| es-es | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-fasterwhisper-zuazo](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper-zuazo) |
| fr-fr | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-citrinet](https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet) |
| gl-es | metric | DMY | N/A | [ovos-stt-plugin-fasterwhisper-zuazo](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper-zuazo) |
| it-it | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-citrinet](https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet) |
| nl-nl | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-citrinet](https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet) |
| pt-br | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-fasterwhisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper) |
| pt-pt | metric | DMY | - https://fasterwhisper.ziggyai.online/stt<br>- https://stt.smartgic.io/fasterwhisper/stt<br>- https://whisper.neonaiservices.com/stt | [ovos-stt-plugin-fasterwhisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper) |

## Voices Overview

These recommendations are meant to cover basic scenarios:
- `offline` - run everything locally, with acceptable latency in a raspberry pi 4
- `online` - use remote servers to offload compute, public or self hosted
- male and female TTS voices availability for `offline` and `online` categories

| Lang | TTS Servers | TTS Plugin | Online Male | Online Female | Offline Male | Offline Female |
| --- | --- | --- | --- | --- | --- | --- |
| ca-ba | - https://tts.smartgic.io/matxa<br>- https://matxa.ziggyai.online | N/A | balear/quim | balear/olga | N/A | N/A |
| ca-es | - https://tts.smartgic.io/matxa<br>- https://matxa.ziggyai.online | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | central/grau | central/elia | upc_pau-x_low | upc_ona-x_low |
| ca-nw | - https://tts.smartgic.io/matxa<br>- https://matxa.ziggyai.online | N/A | nord-occidental/pere | nord-occidental/emma | N/A | N/A |
| ca-va | - https://tts.smartgic.io/matxa<br>- https://matxa.ziggyai.online | N/A | valencia/lluc | valencia/gina | N/A | N/A |
| de-de | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | thorsten-low | ramona-low | thorsten-low | ramona-low |
| en-gb | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | alan-low | N/A | alan-low | alba-medium |
| en-us | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | ryan-low | amy-low | ryan-low | amy-low |
| es-es | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | carlfm-x_low | mls_9972-low | carlfm-x_low | mls_9972-low |
| fr-fr | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | gilles-low | siwis-low | gilles-low | siwis-low |
| gl-es | N/A | [ovos-tts-plugin-cotovia](https://github.com/OpenVoiceOS/ovos-tts-plugin-cotovia) | N/A | N/A | iago | sabela |
| it-it | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | riccardo-x_low | paola-medium | riccardo-x_low | paola-medium |
| nl-nl | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | mls-medium | mls_5809-low | mls-medium | mls_5809-low |
| pt-br | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | faber-medium | N/A | faber-medium | N/A |
| pt-pt | - https://pipertts.ziggyai.online<br>- https://tts.smartgic.io/piper | [ovos-tts-plugin-piper](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper) | tugão-medium | N/A | tugão-medium | N/A |

## Translation Status

in the `tx_info` folder you can find detailed translation stats per language
from [GitLocalize](https://gitlocalize.com/users/OpenVoiceOS) in json and markdown format

> These percentages refer to hardcoded utterances/dialogs in skills and other OVOS components

| Lang  | Translated % |
|-------|--------------|
| ca    | 0.47         |
| pl    | 0.14         |
| gl    | 0.13         |
| es-ES | 0.4          |
| sv    | 0.96         |
| ro-RO | 0.08         |
| da    | 0.96         |
| hu    | 0.96         |
| eu    | 0.0          |
| nl-NL | 0.42         |
| ru    | 0.52         |
| it-IT | 0.69         |
| de-DE | 0.72         |
| pt-BR | 0.24         |
| pt-PT | 0.63         |
| fr-FR | 0.5          |

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

| Plugin                        | Model                                                   | CV7   | CV13    | OpenSLR |
|-------------------------------|---------------------------------------------------------|-------|---------|---------|
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-v2-gl`                             |       | 5.9879  |         |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-large-gl`                                |       | 6.9398  |         |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-medium-gl`                               |       | 7.1227  |         |
| ovos-stt-plugin-wav2vec       | `proxectonos/Nos_ASR-wav2vec2-large-xlsr-53-gl-with-lm` | 15.2  |         | 6.860   |
| ovos-stt-plugin-wav2vec       | `diego-fustes/wav2vec2-large-xlsr-gl`                   | 22.12 |         | 9.10    |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-small-gl`                                |       | 10.9875 |         |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-base-gl`                                 |       | 18.6879 |         |
| ovos-stt-plugin-fasterwhisper | `zuazo/whisper-tiny-gl`                                 |       | 26.3504 |         |       

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
