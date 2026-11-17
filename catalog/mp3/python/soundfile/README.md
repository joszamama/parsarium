# soundfile — MP3 / Python

- **Pinned release:** `0.14.0`
- **License:** BSD-3-Clause
- **Parsed scope:** MP3 header, frame count
- **Underlying family:** libsndfile MP3 decoder
- **Local input API:** `soundfile.info(local path)`
- **Documentation:** [API reference](<https://python-soundfile.readthedocs.io/en/latest/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control verification](../../../../data/python/mp3/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 8000,
  "format": "MP3"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/soundfile/README.md)

```sh
python3 parsarium.py build mp3 python soundfile
python3 parsarium.py run mp3 python soundfile controls/mp3_id3v2/tone-tags.mp3
```
