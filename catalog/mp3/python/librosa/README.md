# librosa — MP3 / Python

- **Pinned release:** `1.0.0`
- **License:** ISC
- **Parsed scope:** decoded PCM sample count
- **Underlying family:** librosa via soundfile/libsndfile
- **Local input API:** `librosa.load(local path, sr=None)`
- **Documentation:** [API reference](<https://librosa.org/doc/main/api/generated/librosa.load.html>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control verification](../../../../data/python/mp3/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "samples": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/python/librosa/README.md)

```sh
python3 parsarium.py build mp3 python librosa
python3 parsarium.py run mp3 python librosa controls/mp3/id3v2-tagged-tone.mp3
```
