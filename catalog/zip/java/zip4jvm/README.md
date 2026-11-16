# zip4jvm — ZIP / Java

- **Pinned release:** `1.13`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** zip4jvm own ZIP parser
- **Local input API:** `UnzipIt.zip(path).stream(name)`
- **Documentation:** [API reference](<https://github.com/oleg-cherednik/zip4jvm>)
- **Catalog evidence:** [parser record](../../../../data/java/zip/parsers.json) · [control verification](../../../../data/java/zip/verification.json) · [within-ecosystem ranking](../../../../data/java/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/java/zip4jvm/README.md)

```sh
python3 parsarium.py build zip java zip4jvm
python3 parsarium.py run zip java zip4jvm controls/zip/hello.zip
```
