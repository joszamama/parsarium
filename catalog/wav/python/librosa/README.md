# librosa — WAV / Python

- **Pinned release:** `1.0.0`
- **Upstream:** [source repository](<https://github.com/librosa/librosa>) · [PyPI](<https://pypi.org/project/librosa/>)
- **License:** ISC
- **Parsed scope:** PCM samples
- **Underlying family:** librosa via soundfile/libsndfile
- **Local input API:** `librosa.load(local path, sr=None)`
- **Documentation:** [API reference](<https://librosa.org/doc/main/api/generated/librosa.load.html>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/librosa/README.md)

```sh
python3 parsarium.py build wav python librosa
python3 parsarium.py run wav python librosa controls/wav/four-samples.wav
```
