# @xhmikosr/decompress — ZIP / JavaScript

- **Pinned release:** `11.1.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `decompress(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@xhmikosr/decompress>)
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

Uses @xhmikosr/decompress-unzip, which uses yauzl.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/xhmikosr_decompress/README.md)

```sh
python3 parsarium.py build zip javascript xhmikosr_decompress
python3 parsarium.py run zip javascript xhmikosr_decompress controls/zip/hello.zip
```
