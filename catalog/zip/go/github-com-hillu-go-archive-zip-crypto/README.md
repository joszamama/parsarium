# github.com/hillu/go-archive-zip-crypto — ZIP / Go

- **Pinned release:** `v0.0.0-20200712202847-bd5cf365dd44`
- **License:** BSD-3-Clause
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip fork
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hillu/go-archive-zip-crypto@v0.0.0-20200712202847-bd5cf365dd44>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

Shared underlying parser lineage or wrapper; package count is not an independent engine count.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_hillu_go_archive_zip_crypto/README.md)

```sh
python3 parsarium.py build zip go github_com_hillu_go_archive_zip_crypto
python3 parsarium.py run zip go github_com_hillu_go_archive_zip_crypto controls/zip/hello.zip
```
