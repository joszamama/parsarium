# archivey — ZIP / Python

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** archivey ZIP reader
- **Local input API:** `archivey.open_archive(path).members(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/archivey/0.3.0/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/python/archivey/README.md)

```sh
python3 parsarium.py build zip python archivey
python3 parsarium.py run zip python archivey controls/zip/hello.zip
```
