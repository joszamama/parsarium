# github.com/gen2brain/go-unarr — ZIP / Go

- **Pinned release:** `v0.2.4`
- **Upstream:** [source repository](<https://github.com/gen2brain/go-unarr>) · [pkg.go.dev](<https://pkg.go.dev/github.com/gen2brain/go-unarr>)
- **License:** Zlib
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** unarr archive backend
- **Local input API:** `NewArchive(path); List(); EntryFor(name); ReadAll()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gen2brain/go-unarr@v0.2.4>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

Unarr-backed multi-format archive reader.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_gen2brain_go_unarr/README.md)

```sh
python3 parsarium.py build zip go github_com_gen2brain_go_unarr
python3 parsarium.py run zip go github_com_gen2brain_go_unarr controls/zip/hello.zip
```
