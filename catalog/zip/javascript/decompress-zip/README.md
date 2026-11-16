# decompress-zip — ZIP / JavaScript

- **Pinned release:** `0.3.3`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** decompress-zip
- **Local input API:** `new DecompressZip(localZipPath).extract({path:target})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/decompress-zip>)
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

[Docker harness and verification receipt](../../../../projects/zip/javascript/decompress_zip/README.md)

```sh
python3 parsarium.py build zip javascript decompress_zip
python3 parsarium.py run zip javascript decompress_zip controls/zip/hello.zip
```
