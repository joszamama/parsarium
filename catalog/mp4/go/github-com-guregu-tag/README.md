# github.com/guregu/tag — MP4 / Go

- **Pinned release:** `v0.0.3`
- **License:** BSD-2-Clause
- **Parsed scope:** MP4 title
- **Underlying family:** dhowden/tag lineage
- **Local input API:** `ReadFrom(io.ReadSeeker)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/guregu/tag@v0.0.3>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_guregu_tag/README.md)

```sh
python3 parsarium.py build mp4 go github_com_guregu_tag
python3 parsarium.py run mp4 go github_com_guregu_tag controls/mp4/red-av.mp4
```
