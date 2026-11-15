# zipfile37 — ZIP / Python

- **Pinned release:** `0.1.3`
- **License:** PSF-2.0
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** CPython zipfile 3.7 backport
- **Local input API:** `zipfile37.ZipFile(path).namelist(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/zipfile37/0.1.3/>)
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
