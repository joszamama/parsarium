# github.com/Sorrow446/go-mp4tag — MP4 / Go

- **Pinned release:** `v0.0.0-20240130220823-68ce31d53e37`
- **License:** MIT
- **Parsed scope:** MP4 title
- **Underlying family:** Sorrow446 MP4 tag reader
- **Local input API:** `Open(local path).Read()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/Sorrow446/go-mp4tag@v0.0.0-20240130220823-68ce31d53e37>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_sorrow446_go_mp4tag/README.md)

```sh
python3 parsarium.py build mp4 go github_com_sorrow446_go_mp4tag
python3 parsarium.py run mp4 go github_com_sorrow446_go_mp4tag controls/mp4/red-av.mp4
```
