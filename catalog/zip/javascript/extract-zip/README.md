# extract-zip — ZIP / JavaScript

- **Pinned release:** `2.0.1`
- **Upstream:** [source repository](<https://github.com/max-mapper/extract-zip>) · [npm](<https://www.npmjs.com/package/extract-zip>)
- **License:** BSD-2-Clause
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `extract(localZipPath, {dir, onEntry})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/extract-zip>)
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

This release depends on yauzl@^2.10.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/extract_zip/README.md)

```sh
python3 parsarium.py build zip javascript extract_zip
python3 parsarium.py run zip javascript extract_zip controls/zip/hello.zip
```
