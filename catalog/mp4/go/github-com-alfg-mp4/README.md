# github.com/alfg/mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20210728035756-55ea58c08aeb`
- **Upstream:** [source repository](<https://github.com/alfg/mp4>) · [pkg.go.dev](<https://pkg.go.dev/github.com/alfg/mp4>)
- **License:** MIT
- **Parsed scope:** major brand
- **Underlying family:** alfg MP4 reader
- **Local input API:** `OpenFromBytes([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/alfg/mp4@v0.0.0-20210728035756-55ea58c08aeb>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_alfg_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_alfg_mp4
python3 parsarium.py run mp4 go github_com_alfg_mp4 controls/mp4/red-av.mp4
```
