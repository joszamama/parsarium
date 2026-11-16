# @loaders.gl/zip — ZIP / JavaScript

- **Pinned release:** `4.5.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** JSZip
- **Local input API:** `ZipLoader.parse(ArrayBuffer)`
- **Documentation:** [API reference](<https://loaders.gl/docs/modules/zip/api-reference/zip-loader>)
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

The ZIP loader wraps JSZip.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/loaders_gl_zip/README.md)

```sh
python3 parsarium.py build zip javascript loaders_gl_zip
python3 parsarium.py run zip javascript loaders_gl_zip controls/zip/hello.zip
```
