# github.com/mholt/archives — ZIP / Go

- **Pinned release:** `v0.1.5`
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** mholt/archives/STARRY-S zip
- **Local input API:** `FileSystem(context,path,nil); fs.ReadFile()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/mholt/archives@v0.1.5>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_mholt_archives/README.md)

```sh
python3 parsarium.py build zip go github_com_mholt_archives
python3 parsarium.py run zip go github_com_mholt_archives controls/zip/hello.zip
```
