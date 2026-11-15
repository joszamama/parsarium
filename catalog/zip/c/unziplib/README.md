# unziplib — ZIP / C

- **Pinned release:** `1.0.0`
- **License:** Apache-2.0 AND Zlib
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** unzipLIB modified classic MiniZip
- **Local input API:** `unzOpen(local ZIP bytes, ZIPFILE); unzGetGlobalInfo; unzGetCurrentFileInfo; unzReadCurrentFile`
- **Documentation:** [API reference](<https://github.com/bitbank2/unzipLIB/blob/1.0.0/src/unzip.h>)
- **Catalog evidence:** [parser record](../../../../data/c/zip/parsers.json) · [control verification](../../../../data/c/zip/verification.json) · [within-ecosystem ranking](../../../../data/c/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Distinct 1.0.0 package with C callback/memory API and bundled zlib; its unzip.h credits Gilles Vollant and shares classic MiniZip lineage. Package license is Apache-2.0 with zlib-licensed bundled code.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
