# github.com/frolovo22/tag — MP4 / Go

- **Pinned release:** `v0.0.2`
- **License:** GPL-3.0
- **Parsed scope:** MP4 title
- **Underlying family:** frolovo22 MP4 tag reader
- **Local input API:** `ReadMp4(io.ReadSeeker).GetTitle()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/frolovo22/tag@v0.0.2>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_frolovo22_tag/README.md)

```sh
python3 parsarium.py build mp4 go github_com_frolovo22_tag
python3 parsarium.py run mp4 go github_com_frolovo22_tag controls/mp4/red-av.mp4
```
