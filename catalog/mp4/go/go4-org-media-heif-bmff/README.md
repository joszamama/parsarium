# go4.org/media/heif/bmff — MP4 / Go

- **Pinned release:** `v0.0.0-20261028031214-ed6929a230fe`
- **Upstream:** [source repository](<https://github.com/go4org/go4>) · [pkg.go.dev](<https://pkg.go.dev/go4.org/media/heif/bmff>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/go4_org_media_heif_bmff/README.md)

```sh
python3 parsarium.py build mp4 go go4_org_media_heif_bmff
python3 parsarium.py run mp4 go go4_org_media_heif_bmff controls/mp4/red-av.mp4
```
