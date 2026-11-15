# pclzip/pclzip — ZIP / PHP

- **Pinned release:** `2.8.2`
- **License:** LGPL-2.1
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** PclZip PHP ZIP reader
- **Local input API:** `PclZip(local path); extract(PCLZIP_OPT_EXTRACT_AS_STRING)`
- **Documentation:** [API reference](<https://github.com/ivanlanin/pclzip/blob/19dd1de9d3f5fc4d7d70175b4c344dee329f45fd/pclzip.lib.php>)
- **Catalog evidence:** [parser record](../../../../data/php/zip/parsers.json) · [control verification](../../../../data/php/zip/verification.json) · [within-ecosystem ranking](../../../../data/php/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Pure PHP ZIP archive parser with zlib decompression; isolated Composer install because UnifiedArchive declares it replaces pclzip/pclzip.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/pclzip/README.md)

```sh
python3 parsarium.py build zip php pclzip
python3 parsarium.py run zip php pclzip controls/zip/hello.zip
```
