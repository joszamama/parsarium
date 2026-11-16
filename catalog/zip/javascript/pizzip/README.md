# pizzip — ZIP / JavaScript

- **Pinned release:** `3.3.0`
- **License:** MIT OR GPL-3.0
- **Parsed scope:** entries_and_content
- **Underlying family:** JSZip
- **Local input API:** `new PizZip(Buffer); zip.file(name).asText()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pizzip>)
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

Fork of JSZip 2.x.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/pizzip/README.md)

```sh
python3 parsarium.py build zip javascript pizzip
python3 parsarium.py run zip javascript pizzip controls/zip/hello.zip
```
