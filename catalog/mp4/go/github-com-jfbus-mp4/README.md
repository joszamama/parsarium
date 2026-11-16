# github.com/jfbus/mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20150401112544-b5bc0819ce33`
- **License:** MIT
- **Parsed scope:** ftyp brand only
- **Underlying family:** jfbus MP4 lineage
- **Local input API:** `DecodeHeader(io.Reader); DecodeFtyp(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/jfbus/mp4@v0.0.0-20150401112544-b5bc0819ce33>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom"
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_jfbus_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_jfbus_mp4
python3 parsarium.py run mp4 go github_com_jfbus_mp4 controls/mp4/red-av.mp4
```
