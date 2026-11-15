# github.com/klauspost/compress/zip — ZIP / Go

- **Pinned release:** `v1.20.4`
- **License:** Apache-2.0, BSD-3-Clause, MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip fork
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/klauspost/compress/zip@v1.20.4>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/klauspost_compress_zip/README.md)

```sh
python3 parsarium.py build zip go klauspost_compress_zip
python3 parsarium.py run zip go klauspost_compress_zip controls/zip/hello.zip
```
