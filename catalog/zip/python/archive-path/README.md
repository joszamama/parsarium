# archive-path — ZIP / Python

- **Pinned release:** `0.4.2`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** archive-path via CPython zipfile
- **Local input API:** `archive_path.ZipPath(path).iterdir(); read_bytes()`
- **Documentation:** [API reference](<https://pypi.org/project/archive-path/0.4.2/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/archive_path/README.md)

```sh
python3 parsarium.py build zip python archive_path
python3 parsarium.py run zip python archive_path controls/zip/hello.zip
```
