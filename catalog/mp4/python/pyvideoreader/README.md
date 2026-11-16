# pyvideoreader — MP4 / Python

- **Pinned release:** `0.5.7`
- **License:** MIT
- **Parsed scope:** video dimensions and first-frame channel count
- **Underlying family:** pyvideoreader via OpenCV
- **Local input API:** `videoreader.VideoReader(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pyvideoreader/0.5.7/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "frames": 1,
  "width": 2,
  "height": 2,
  "channels": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/pyvideoreader/README.md)

```sh
python3 parsarium.py build mp4 python pyvideoreader
python3 parsarium.py run mp4 python pyvideoreader controls/mp4/red-av.mp4
```
