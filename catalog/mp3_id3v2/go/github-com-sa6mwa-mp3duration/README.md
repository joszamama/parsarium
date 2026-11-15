# github.com/sa6mwa/mp3duration — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.0-20221104103912-0716b1a5de6e`
- **License:** MIT
- **Parsed scope:** reported duration and frame count
- **Underlying family:** sa6mwa MP3 duration reader
- **Local input API:** `ReadFile(local path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/sa6mwa/mp3duration@v0.0.0-20221104103912-0716b1a5de6e>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "duration_ms": 1071,
  "frames": 41
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
