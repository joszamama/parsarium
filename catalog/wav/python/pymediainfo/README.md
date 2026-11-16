# pymediainfo — WAV / Python

- **Pinned release:** `7.0.1`
- **License:** MIT
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** MediaInfo native WAV parser
- **Local input API:** `pymediainfo.MediaInfo.parse(local path).tracks`
- **Documentation:** [API reference](<https://pypi.org/project/pymediainfo/7.0.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/pymediainfo/README.md)

```sh
python3 parsarium.py build wav python pymediainfo
python3 parsarium.py run wav python pymediainfo controls/wav/four-samples.wav
```
