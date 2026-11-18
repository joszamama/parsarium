# github.com/MStoykov/mp4 — MP4 / Go

- **Pinned release:** `v0.1.4`
- **Upstream:** [source repository](<https://github.com/mstoykov/mp4>) · [pkg.go.dev](<https://pkg.go.dev/github.com/MStoykov/mp4>)
- **License:** MIT
- **Parsed scope:** major brand
- **Underlying family:** jfbus MP4 lineage
- **Local input API:** `Decode(RangeReader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/MStoykov/mp4@v0.1.4>)
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

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_mstoykov_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_mstoykov_mp4
python3 parsarium.py run mp4 go github_com_mstoykov_mp4 controls/mp4/red-av.mp4
```
