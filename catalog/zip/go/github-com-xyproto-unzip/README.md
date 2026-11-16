# github.com/xyproto/unzip — ZIP / Go

- **Pinned release:** `v1.0.1`
- **License:** BSD-3-Clause
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `Extract(path,destination)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/xyproto/unzip@v1.0.1>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_xyproto_unzip/README.md)

```sh
python3 parsarium.py build zip go github_com_xyproto_unzip
python3 parsarium.py run zip go github_com_xyproto_unzip controls/zip/hello.zip
```
