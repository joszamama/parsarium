# libarchive-c — ZIP / Python

- **Pinned release:** `5.3`
- **License:** CC0-1.0
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** native libarchive
- **Local input API:** `libarchive.file_reader(path); entry.pathname; get_blocks()`
- **Documentation:** [API reference](<https://github.com/Changaco/python-libarchive-c>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/libarchive_c/README.md)

```sh
python3 parsarium.py build zip python libarchive_c
python3 parsarium.py run zip python libarchive_c controls/zip/hello.zip
```
