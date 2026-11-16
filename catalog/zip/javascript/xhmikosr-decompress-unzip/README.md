# @xhmikosr/decompress-unzip — ZIP / JavaScript

- **Pinned release:** `8.2.1`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `decompressUnzip()(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@xhmikosr/decompress-unzip>)
- **Catalog evidence:** [parser record](../../../../data/javascript/zip/parsers.json) · [control verification](../../../../data/javascript/zip/verification.json) · [within-ecosystem ranking](../../../../data/javascript/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": [
    "hello.txt"
  ],
  "content": "parsarium\n"
}
```

The pinned release depends on yauzl@^3.4.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/xhmikosr_decompress_unzip/README.md)

```sh
python3 parsarium.py build zip javascript xhmikosr_decompress_unzip
python3 parsarium.py run zip javascript xhmikosr_decompress_unzip controls/zip/hello.zip
```
