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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
