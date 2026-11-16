# github.com/unknwon/cae/zip — ZIP / Go

- **Pinned release:** `v1.0.2`
- **License:** Apache-2.0
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `ExtractTo(path,destination)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unknwon/cae/zip@v1.0.2>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_unknwon_cae_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_unknwon_cae_zip
python3 parsarium.py run zip go github_com_unknwon_cae_zip controls/zip/hello.zip
```
