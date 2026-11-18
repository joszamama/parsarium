# av — WAV / Python

- **Pinned release:** `19.0.2`
- **Upstream:** [source repository](<https://github.com/PyAV-Org/PyAV>) · [PyPI](<https://pypi.org/project/av/>)
- **License:** BSD-3-Clause
- **Parsed scope:** PCM samples
- **Underlying family:** FFmpeg libavformat/libavcodec via PyAV
- **Local input API:** `av.open(local path).decode(audio=0)`
- **Documentation:** [API reference](<https://pyav.org/docs/stable/api/container.html>)
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

[Docker harness and verification receipt](../../../../projects/wav/python/av/README.md)

```sh
python3 parsarium.py build wav python av
python3 parsarium.py run wav python av controls/wav/four-samples.wav
```
