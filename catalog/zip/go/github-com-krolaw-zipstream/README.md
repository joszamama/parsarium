# github.com/krolaw/zipstream — ZIP / Go

- **Pinned release:** `v0.0.0-20241109034754-4a67be70fe31`
- **License:** BSD-3-Clause
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** zipstream
- **Local input API:** `NewReader(io.Reader); Reader.Next(); Read()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/krolaw/zipstream>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/go/github_com_krolaw_zipstream/README.md)

```sh
python3 parsarium.py build zip go github_com_krolaw_zipstream
python3 parsarium.py run zip go github_com_krolaw_zipstream controls/zip/hello.zip
```
