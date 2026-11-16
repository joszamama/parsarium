# zipfile-zstd — ZIP / Python

- **Pinned release:** `0.0.4`
- **License:** MIT
- **Parsed scope:** Zstandard ZIP method 93 entry name and content
- **Underlying family:** CPython zipfile plus zstandard codec
- **Local input API:** `zipfile_zstd.ZipFile(path); getinfo(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/zipfile-zstd/0.0.4/>)
- **Catalog evidence:** [parser record](../../../../data/python/zip/parsers.json) · [control verification](../../../../data/python/zip/verification.json) · [within-ecosystem ranking](../../../../data/python/zip/ranking.md)
- **Valid control:** [`controls/zip/hello-zstd.zip`](../../../../controls/zip/hello-zstd.zip)

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

[Docker harness and verification receipt](../../../../projects/zip/python/zipfile_zstd/README.md)

```sh
python3 parsarium.py build zip python zipfile_zstd
python3 parsarium.py run zip python zipfile_zstd controls/zip/hello-zstd.zip
```
