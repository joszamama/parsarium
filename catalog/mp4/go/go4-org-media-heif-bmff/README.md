# go4.org/media/heif/bmff — MP4 / Go

- **Pinned release:** `v0.0.0-20261028031214-ed6929a230fe`
- **License:** Apache-2.0
- **Parsed scope:** ftyp brand only
- **Underlying family:** go4 ISO BMFF reader
- **Local input API:** `NewReader(io.Reader).ReadAndParseBox(TypeFtyp)`
- **Documentation:** [API reference](<https://pkg.go.dev/go4.org/media/heif/bmff@v0.0.0-20261028031214-ed6929a230fe>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
