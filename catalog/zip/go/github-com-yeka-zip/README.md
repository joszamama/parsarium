# github.com/yeka/zip — ZIP / Go

- **Pinned release:** `v0.0.0-20231116150916-03d6312748a9`
- **Upstream:** [source repository](<https://github.com/yeka/zip>) · [pkg.go.dev](<https://pkg.go.dev/github.com/yeka/zip>)
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** yeka/alexmullins ZIP lineage
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/yeka/zip@v0.0.0-20231116150916-03d6312748a9>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_yeka_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_yeka_zip
python3 parsarium.py run zip go github_com_yeka_zip controls/zip/hello.zip
```
