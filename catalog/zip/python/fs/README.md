# fs — ZIP / Python

- **Pinned release:** `2.4.16`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** PyFilesystem ZipFS via CPython zipfile
- **Local input API:** `fs.zipfs.ZipFS(path).listdir(); readbytes()`
- **Documentation:** [API reference](<https://github.com/PyFilesystem/pyfilesystem2/blob/master/fs/zipfs.py>)
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
