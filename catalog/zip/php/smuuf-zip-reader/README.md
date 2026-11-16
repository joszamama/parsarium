# smuuf/zip-reader — ZIP / PHP

- **Pinned release:** `1.0`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Smuuf ZIP reader over PHP ZipArchive
- **Local input API:** `ZipReader(local path); browse root; getEntries; ZippedFile::read`
- **Documentation:** [API reference](<https://github.com/smuuf/php-zip-reader/blob/363eaa22a52be72a2dc3fc6c3bef78835da4f259/README.md>)
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

Opens the local ZIP with PHP ZipArchive and exposes a navigable entry tree.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/smuuf_zip_reader/README.md)

```sh
python3 parsarium.py build zip php smuuf_zip_reader
python3 parsarium.py run zip php smuuf_zip_reader controls/zip/hello.zip
```
