# ffmpeg-python — MP4 / Python

- **Pinned release:** `0.2.0`
- **License:** Apache-2.0
- **Parsed scope:** video dimensions, codec, title
- **Underlying family:** ffmpeg-python via external FFprobe
- **Local input API:** `ffmpeg.probe(local path)`
- **Documentation:** [API reference](<https://github.com/kkroening/ffmpeg-python>)
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
