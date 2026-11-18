# scipy — WAV / Python

- **Pinned release:** `1.18.1`
- **Upstream:** [source repository](<https://github.com/scipy/scipy>) · [PyPI](<https://pypi.org/project/scipy/>)
- **License:** BSD-3-Clause
- **Parsed scope:** PCM samples
- **Underlying family:** SciPy WAV parser
- **Local input API:** `scipy.io.wavfile.read(local path)`
- **Documentation:** [API reference](<https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html>)
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

[Docker harness and verification receipt](../../../../projects/wav/python/scipy/README.md)

```sh
python3 parsarium.py build wav python scipy
python3 parsarium.py run wav python scipy controls/wav/four-samples.wav
```
