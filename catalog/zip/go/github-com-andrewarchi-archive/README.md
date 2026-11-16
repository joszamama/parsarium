# github.com/andrewarchi/archive — ZIP / Go

- **Pinned release:** `v0.0.0-20210213193640-3a6449eed2ec`
- **License:** MPL-2.0
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `OpenSingleFileZip(path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/andrewarchi/archive@v0.0.0-20210213193640-3a6449eed2ec>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_andrewarchi_archive/README.md)

```sh
python3 parsarium.py build zip go github_com_andrewarchi_archive
python3 parsarium.py run zip go github_com_andrewarchi_archive controls/zip/hello.zip
```
