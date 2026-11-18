# github.com/evilsocket/islazy/zip — ZIP / Go

- **Pinned release:** `v1.11.0`
- **Upstream:** [source repository](<https://github.com/evilsocket/islazy>) · [pkg.go.dev](<https://pkg.go.dev/github.com/evilsocket/islazy/zip>)
- **License:** GPL-3.0
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `Unzip(path,destination)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/evilsocket/islazy/zip@v1.11.0>)
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

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_evilsocket_islazy_zip/README.md)

```sh
python3 parsarium.py build zip go github_com_evilsocket_islazy_zip
python3 parsarium.py run zip go github_com_evilsocket_islazy_zip controls/zip/hello.zip
```
