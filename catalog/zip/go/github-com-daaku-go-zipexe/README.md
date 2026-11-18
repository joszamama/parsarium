# github.com/daaku/go.zipexe — ZIP / Go

- **Pinned release:** `v1.0.2`
- **Upstream:** [source repository](<https://github.com/daaku/go.zipexe>) · [pkg.go.dev](<https://pkg.go.dev/github.com/daaku/go.zipexe>)
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `OpenCloser(path); zip.Reader.File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/daaku/go.zipexe@v1.0.2>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

Wrapper over Go archive/zip.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_daaku_go_zipexe/README.md)

```sh
python3 parsarium.py build zip go github_com_daaku_go_zipexe
python3 parsarium.py run zip go github_com_daaku_go_zipexe controls/zip/hello.zip
```
