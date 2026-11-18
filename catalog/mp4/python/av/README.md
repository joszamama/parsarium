# av — MP4 / Python

- **Pinned release:** `19.0.2`
- **Upstream:** [source repository](<https://github.com/PyAV-Org/PyAV>) · [PyPI](<https://pypi.org/project/av/>)
- **License:** BSD-3-Clause
- **Parsed scope:** video/audio tracks and title
- **Underlying family:** FFmpeg libavformat via PyAV
- **Local input API:** `av.open(local path)`
- **Documentation:** [API reference](<https://pyav.org/docs/stable/api/container.html>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "video_codec": "h264",
  "audio_codec": "aac"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/av/README.md)

```sh
python3 parsarium.py build mp4 python av
python3 parsarium.py run mp4 python av controls/mp4/red-av.mp4
```
