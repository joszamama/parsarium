# madnest/madzipper — ZIP / PHP

- **Pinned release:** `1.6.0`
- **Upstream:** [source repository](<https://github.com/madnest/madzipper>) · [Packagist](<https://packagist.org/packages/madnest/madzipper>)
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Madnest Madzipper over PHP ZipArchive
- **Local input API:** `Madzipper::make(local ZIP path); listFiles; getFileContent`
- **Documentation:** [API reference](<https://github.com/madnest/madzipper/blob/527c35105820a0b4c8cfdadd3f475b26d62d9ac2/README.md>)
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

A fork of Chumper Zipper with its own Composer package API; delegates archive parsing to PHP ZipArchive.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/madnest_madzipper/README.md)

```sh
python3 parsarium.py build zip php madnest_madzipper
python3 parsarium.py run zip php madnest_madzipper controls/zip/hello.zip
```
