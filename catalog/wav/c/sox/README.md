# sox — WAV / C

- **Pinned release:** `14.4.2`
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** SoX libsox WAV reader
- **Local input API:** `sox_init; sox_open_read(local WAV path); sox_read decoded samples; sox_sample_t conversion; sox_close`
- **Documentation:** [API reference](<https://github.com/chirlu/sox/blob/master/libsox.3>)
- **Catalog evidence:** [parser record](../../../../data/c/wav/parsers.json) · [control verification](../../../../data/c/wav/verification.json) · [within-ecosystem ranking](../../../../data/c/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

SoX public libsox audio file API reads RIFF/WAVE and decoded samples; pinned source release is the primary SourceForge package.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/c/sox/README.md)

```sh
python3 parsarium.py build wav c sox
python3 parsarium.py run wav c sox controls/wav/four-samples.wav
```
