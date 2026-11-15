# github.com/unxed/zip — ZIP / Go

- **Pinned release:** `v0.1.146`
- **License:** BSD-3-Clause
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** unxed ZIP
- **Local input API:** `OpenReader(path); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unxed/zip@v0.1.146>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
