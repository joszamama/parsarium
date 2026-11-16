# omni-archive — ZIP / Python

- **Pinned release:** `0.0.2`
- **License:** GPL-3.0-only
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** omni-archive via CPython zipfile
- **Local input API:** `omni_archive.Archive(path).members(); open_member()`
- **Documentation:** [API reference](<https://pypi.org/project/omni-archive/0.0.2/>)
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
