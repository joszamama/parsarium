# quazip — ZIP / C++

- **Pinned release:** `1.7.2`
- **License:** LGPL-2.1-only
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** QuaZip wrapper over classic MiniZip
- **Local input API:** `QuaZip(local filename); open(mdUnzip); getFileNameList; setCurrentFile; QuaZipFile::readAll`
- **Documentation:** [API reference](<https://github.com/stachenov/quazip/blob/v1.7.2/quazip/quazip.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/zip/parsers.json) · [control verification](../../../../data/cpp/zip/verification.json) · [within-ecosystem ranking](../../../../data/cpp/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Distinct Qt/C++ package API backed by classic MiniZip, sharing decoder lineage with minizip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
