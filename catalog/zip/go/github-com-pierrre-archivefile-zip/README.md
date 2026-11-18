# github.com/pierrre/archivefile/zip — ZIP / Go

- **Pinned release:** `v0.0.0-20170218184037-e2d100bc74f5`
- **Upstream:** [source repository](<https://github.com/pierrre/archivefile>) · [pkg.go.dev](<https://pkg.go.dev/github.com/pierrre/archivefile/zip>)
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `UnarchiveFile(path,destination,nil)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pierrre/archivefile/zip@v0.0.0-20170218184037-e2d100bc74f5>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_pierrre_archivefile_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_pierrre_archivefile_zip
python3 parsarium.py run zip go github_com_pierrre_archivefile_zip controls/zip/hello.zip
```
