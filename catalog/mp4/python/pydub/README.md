# pydub — MP4 / Python

- **Pinned release:** `0.25.1`
- **License:** MIT
- **Parsed scope:** AAC audio decode
- **Underlying family:** pydub via FFmpeg
- **Local input API:** `pydub.AudioSegment.from_file(local path)`
- **Documentation:** [API reference](<https://github.com/jiaaro/pydub>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "audio_rate": 8000,
  "audio_channels": 1,
  "duration_ms": 1000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
