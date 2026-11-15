# miniaudio — MP3 with ID3v2 / Python

- **Pinned release:** `1.73`
- **License:** MIT
- **Parsed scope:** decoded PCM sample count
- **Underlying family:** miniaudio native MP3 decoder
- **Local input API:** `miniaudio.mp3_read_f32(local bytes)`
- **Documentation:** [API reference](<https://pypi.org/project/miniaudio/1.73/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
