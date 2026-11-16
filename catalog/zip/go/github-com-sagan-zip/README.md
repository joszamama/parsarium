# github.com/sagan/zip — ZIP / Go

- **Pinned release:** `v0.0.0-20240708090818-02b11188bf71`
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** yeka/alexmullins ZIP lineage
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/sagan/zip@v0.0.0-20240708090818-02b11188bf71>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_sagan_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_sagan_zip
python3 parsarium.py run zip go github_com_sagan_zip controls/zip/hello.zip
```
