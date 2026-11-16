# simplezip — ZIP / Java

- **Pinned release:** `2.2`
- **License:** ISC
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** SimpleZip own ZIP parser
- **Local input API:** `new ZipFileInput(file).readFileHeader(); readFileData(output)`
- **Documentation:** [API reference](<https://256stuff.com/sources/simplezip/docs/simplezip.pdf>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/simplezip/README.md)

```sh
python3 parsarium.py build zip java simplezip
python3 parsarium.py run zip java simplezip controls/zip/hello.zip
```
