# github.com/frolovo22/tag — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.2`
- **License:** GPL-3.0
- **Parsed scope:** ID3v2.3 title with trailing NUL
- **Underlying family:** frolovo22 ID3 parser
- **Local input API:** `ReadID3v23(io.ReadSeeker).GetTitle()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/frolovo22/tag@v0.0.2>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium\u0000"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
