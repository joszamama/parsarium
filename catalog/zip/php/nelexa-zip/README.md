# nelexa/zip — ZIP / PHP

- **Pinned release:** `4.0.2`
- **Upstream:** [source repository](<https://github.com/Ne-Lexa/php-zip>) · [Packagist](<https://packagist.org/packages/nelexa/zip>)
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Ne-Lexa pure PHP ZIP reader
- **Local input API:** `ZipFile::openFile(local path); getListFiles; getEntryContents`
- **Documentation:** [API reference](<https://github.com/Ne-Lexa/php-zip/blob/88a1b6549be813278ff2dd3b6b2ac188827634a7/README.md>)
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

Parses ZIP records in PHP and uses compression primitives; no ZipArchive dependency observed.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/nelexa_zip/README.md)

```sh
python3 parsarium.py build zip php nelexa_zip
python3 parsarium.py run zip php nelexa_zip controls/zip/hello.zip
```
