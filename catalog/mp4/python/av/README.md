# av — MP4 / Python

- **Pinned release:** `19.0.2`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
