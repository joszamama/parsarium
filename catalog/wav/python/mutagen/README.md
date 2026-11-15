# mutagen — WAV / Python

- **Pinned release:** `1.48.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** Mutagen WAVE parser
- **Local input API:** `mutagen.wave.WAVE(local path).info`
- **Documentation:** [API reference](<https://mutagen.readthedocs.io/en/latest/api/wave.html>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/mutagen/README.md)

```sh
python3 parsarium.py build wav python mutagen
python3 parsarium.py run wav python mutagen controls/wav/four-samples.wav
```
