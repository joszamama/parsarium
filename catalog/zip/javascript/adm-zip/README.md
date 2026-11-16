# adm-zip — ZIP / JavaScript

- **Pinned release:** `0.6.1`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** ADM-ZIP
- **Local input API:** `new AdmZip(Buffer); getEntries(); readAsText(entry)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/adm-zip>)
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

[Docker harness and verification receipt](../../../../projects/zip/javascript/adm_zip/README.md)

```sh
python3 parsarium.py build zip javascript adm_zip
python3 parsarium.py run zip javascript adm_zip controls/zip/hello.zip
```
