# jszip — ZIP / JavaScript

- **Pinned release:** `3.10.2`
- **License:** MIT OR GPL-3.0-or-later
- **Parsed scope:** entries_and_content
- **Underlying family:** JSZip
- **Local input API:** `JSZip.loadAsync(Buffer); zip.file(name).async('string')`
- **Documentation:** [API reference](<https://github.com/Stuk/jszip/blob/main/documentation/api_jszip/load_async.md>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/jszip/README.md)

```sh
python3 parsarium.py build zip javascript jszip
python3 parsarium.py run zip javascript jszip controls/zip/hello.zip
```
