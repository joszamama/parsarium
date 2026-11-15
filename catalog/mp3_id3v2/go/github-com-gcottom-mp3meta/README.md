# github.com/gcottom/mp3meta — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.4`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** gcottom MP3 tag reader
- **Local input API:** `ParseMP3(io.ReadSeeker)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gcottom/mp3meta@v0.0.4>)
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
