# github.com/tosone/minimp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v1.1.0`
- **License:** MIT
- **Parsed scope:** decoded PCM bytes and audio format
- **Underlying family:** minimp3 decoder
- **Local input API:** `DecodeFull([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tosone/minimp3@v1.1.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "decoded_bytes": 94464
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
