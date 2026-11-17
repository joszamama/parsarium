# github.com/bogem/id3v2/v2 — MP3 / Go

- **Pinned release:** `v2.1.4`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title
- **Underlying family:** bogem ID3v2 parser
- **Local input API:** `ParseReader(io.Reader,Options{Parse:true}).Title()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/bogem/id3v2/v2@v2.1.4>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-44k.mp3`](../../../../controls/mp3/id3v2-tagged-tone-44k.mp3)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/go/github_com_bogem_id3v2_v2/README.md)

```sh
python3 parsarium.py build mp3 go github_com_bogem_id3v2_v2
python3 parsarium.py run mp3 go github_com_bogem_id3v2_v2 controls/mp3/id3v2-tagged-tone-44k.mp3
```
