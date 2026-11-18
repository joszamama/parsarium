# github.com/c4milo/unpackit — ZIP / Go

- **Pinned release:** `v1.0.0`
- **Upstream:** [source repository](<https://github.com/c4milo/unpackit>) · [pkg.go.dev](<https://pkg.go.dev/github.com/c4milo/unpackit>)
- **License:** MPL-2.0
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `Unzip(io.Reader,destination)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/c4milo/unpackit@v1.0.0>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_c4milo_unpackit/README.md)

```sh
python3 parsarium.py build zip go github_com_c4milo_unpackit
python3 parsarium.py run zip go github_com_c4milo_unpackit controls/zip/hello.zip
```
