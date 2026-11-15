# pyzip — ZIP / Python

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** pyzip via CPython zipfile
- **Local input API:** `pyzip.PyZip().from_file(path).zip_content`
- **Documentation:** [API reference](<https://pypi.org/project/pyzip/0.3.0/>)
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
