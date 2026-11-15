# github.com/fgergo/mp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v1.0.0`
- **License:** MIT
- **Parsed scope:** MPEG frame size and samples
- **Underlying family:** tcolgate MP3 frame lineage
- **Local input API:** `NewDecoder(io.Reader).Decode(*Frame,*int)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/fgergo/mp3@v1.0.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "frame_bytes": 208,
  "samples": 1152
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
