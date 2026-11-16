# sempia/getid3 — WAV / PHP

- **Pinned release:** `2.0.0.0-p1.9.25`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `JamesHeinrich\GetID3\GetID3::analyze(local PCM WAV path); fileformat and audio sample rate/channels/bit depth`
- **Documentation:** [API reference](<https://gitlab.com/Sempia/getID3/-/blob/46405ae39a503ac72d1ce5b31f6f11f938f034ed/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "fileformat": "wav",
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16
}
```

Namespaced getID3 fork; distinct Composer package path and shared parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/sempia_getid3/README.md)

```sh
python3 parsarium.py build wav php sempia_getid3
python3 parsarium.py run wav php sempia_getid3 controls/wav/256-samples.wav
```
