# pydub — WAV / Python

- **Pinned release:** `0.25.1`
- **Upstream:** [source repository](<https://github.com/jiaaro/pydub>) · [PyPI](<https://pypi.org/project/pydub/>)
- **License:** MIT
- **Parsed scope:** PCM samples
- **Underlying family:** pydub native WAV header parser
- **Local input API:** `pydub.AudioSegment.from_wav(local path)`
- **Documentation:** [API reference](<https://github.com/jiaaro/pydub>)
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

[Docker harness and verification receipt](../../../../projects/wav/python/pydub/README.md)

```sh
python3 parsarium.py build wav python pydub
python3 parsarium.py run wav python pydub controls/wav/four-samples.wav
```
