# patool — ZIP / Python

- **Pinned release:** `4.1.0`
- **License:** GPL-3.0-only
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** patool via local unzip utility
- **Local input API:** `patoolib.extract_archive(path, outdir=destination)`
- **Documentation:** [API reference](<https://pypi.org/project/patool/4.1.0/>)
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
