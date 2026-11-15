# james-heinrich/getid3 — WAV / PHP

- **Pinned release:** `v1.9.28`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `getID3::analyze(local PCM WAV path); fileformat, audio sample_rate/channels/bits_per_sample`
- **Documentation:** [API reference](<https://github.com/JamesHeinrich/getID3/blob/be83ea6ffbdac0301d83bee0d42f09e2a41bd0dd/README.md>)
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

Own getID3 RIFF/WAVE reader; same package release and Composer lock are shared with the PHP MP3 cell.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/getid3/README.md)

```sh
python3 parsarium.py build wav php getid3
python3 parsarium.py run wav php getid3 controls/wav/256-samples.wav
```
