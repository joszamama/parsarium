# audioread — MP3 with ID3v2 / Python

- **Pinned release:** `3.1.0`
- **License:** MIT
- **Parsed scope:** MP3 duration and audio properties
- **Underlying family:** audioread via FFmpeg
- **Local input API:** `audioread.audio_open(local path)`
- **Documentation:** [API reference](<https://github.com/beetbox/audioread>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "duration_seconds": 1.152
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
