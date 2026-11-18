# github.com/dhowden/tag — MP3 / Go

- **Pinned release:** `v0.0.0-20240417053706-3d75831295e8`
- **Upstream:** [source repository](<https://github.com/dhowden/tag>) · [pkg.go.dev](<https://pkg.go.dev/github.com/dhowden/tag>)
- **License:** BSD-2-Clause
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** dhowden/tag lineage
- **Local input API:** `ReadFrom(io.ReadSeeker).Title()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-44k.mp3`](../../../../controls/mp3/id3v2-tagged-tone-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/go/github_com_dhowden_tag/README.md)

```sh
python3 parsarium.py build mp3 go github_com_dhowden_tag
python3 parsarium.py run mp3 go github_com_dhowden_tag controls/mp3/id3v2-tagged-tone-44k.mp3
```
