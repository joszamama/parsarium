# github.com/unxed/zip — ZIP / Go

- **Pinned release:** `v0.1.146`
- **License:** BSD-3-Clause
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** unxed ZIP
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unxed/zip@v0.1.146>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_unxed_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_unxed_zip
python3 parsarium.py run zip go github_com_unxed_zip controls/zip/hello.zip
```
