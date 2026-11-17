# github.com/ascherkus/go-id3/src/id3 — MP3 / Go

- **Pinned release:** `v0.0.0-20120522061058-b139b6a612de`
- **License:** Apache-2.0
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** ascherkus/go-id3 lineage
- **Local input API:** `Read(io.Reader).Name`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ascherkus/go-id3/src/id3@v0.0.0-20120522061058-b139b6a612de>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_ascherkus_go_id3_src_id3/README.md)

```sh
python3 parsarium.py build mp3 go github_com_ascherkus_go_id3_src_id3
python3 parsarium.py run mp3 go github_com_ascherkus_go_id3_src_id3 controls/mp3_id3v2/tone-tags-44k.mp3
```
