# wikimedia/getid3 — WAV / PHP

- **Pinned release:** `v2.0.0-beta5`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `JamesHeinrich\GetID3\GetID3::analyze(local PCM WAV path); fileformat and audio sample rate/channels/bit depth`
- **Documentation:** [API reference](<https://github.com/wikimedia/getID3/blob/4e7aca96e7f4cf5ce6e08bca998334f567259965/README.md>)
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

Wikimedia fork of namespaced getID3; distinct Composer package path and shared parser lineage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
