# github.com/qiniu/audio/mp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v0.2.1`
- **License:** Apache-2.0
- **Parsed scope:** decoded PCM bytes and audio format
- **Underlying family:** hajime/go-mp3 wrapper
- **Local input API:** `Decode(io.ReadSeeker); Read([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/qiniu/audio/mp3@v0.2.1>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 2,
  "decoded_bytes": 64
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
