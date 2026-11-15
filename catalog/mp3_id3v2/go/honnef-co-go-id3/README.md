# honnef.co/go/id3 — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.0-20250113165337-e36fa5d059c5`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** honnef ID3 parser
- **Local input API:** `NewDecoder(io.Reader).Parse().Title()`
- **Documentation:** [API reference](<https://pkg.go.dev/honnef.co/go/id3@v0.0.0-20250113165337-e36fa5d059c5>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
