# github.com/guregu/tag — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.3`
- **License:** BSD-2-Clause
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** dhowden/tag lineage
- **Local input API:** `ReadFrom(io.ReadSeeker).Title()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/guregu/tag@v0.0.3>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_guregu_tag/README.md)

```sh
python3 parsarium.py build mp3_id3v2 go github_com_guregu_tag
python3 parsarium.py run mp3_id3v2 go github_com_guregu_tag controls/mp3_id3v2/tone-tags-44k.mp3
```
