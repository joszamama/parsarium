# github.com/gcottom/mp4meta — MP4 / Go

- **Pinned release:** `v0.0.5`
- **License:** MIT
- **Parsed scope:** MP4 title
- **Underlying family:** gcottom MP4 tag reader
- **Local input API:** `ReadMP4(io.ReadSeeker)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gcottom/mp4meta@v0.0.5>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_gcottom_mp4meta/README.md)

```sh
python3 parsarium.py build mp4 go github_com_gcottom_mp4meta
python3 parsarium.py run mp4 go github_com_gcottom_mp4meta controls/mp4/red-av.mp4
```
