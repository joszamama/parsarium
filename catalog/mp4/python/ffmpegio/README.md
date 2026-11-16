# ffmpegio — MP4 / Python

- **Pinned release:** `0.12.0`
- **License:** GPL-2.0-only
- **Parsed scope:** video dimensions, codec, title
- **Underlying family:** ffmpegio via external FFprobe
- **Local input API:** `ffmpegio.probe.full_details(local path)`
- **Documentation:** [API reference](<https://python-ffmpegio.github.io/python-ffmpegio/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "video_codec": "h264"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/ffmpegio/README.md)

```sh
python3 parsarium.py build mp4 python ffmpegio
python3 parsarium.py run mp4 python ffmpegio controls/mp4/red-av.mp4
```
