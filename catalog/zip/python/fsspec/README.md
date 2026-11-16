# fsspec — ZIP / Python

- **Pinned release:** `2026.9.0`
- **License:** BSD-3-Clause
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** fsspec ZipFileSystem via CPython zipfile
- **Local input API:** `fsspec.filesystem("zip", fo=path).ls(); open()`
- **Documentation:** [API reference](<https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.implementations.zip.ZipFileSystem>)
- **Catalog evidence:** [parser record](../../../../data/python/zip/parsers.json) · [control verification](../../../../data/python/zip/verification.json) · [within-ecosystem ranking](../../../../data/python/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "names": [
    "hello.txt"
  ],
  "hello": "parsarium\n"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
