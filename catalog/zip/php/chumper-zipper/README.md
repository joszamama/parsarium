# chumper/zipper — ZIP / PHP

- **Pinned release:** `v1.0.3`
- **License:** Apache2
- **Parsed scope:** decompressed bytes of a named entry
- **Underlying family:** Chumper Zipper over PHP ZipArchive
- **Local input API:** `Zipper::make(local ZIP path); getFileContent(known control entry name)`
- **Documentation:** [API reference](<https://github.com/Chumper/Zipper/blob/d15207e010f8fe1bdd341376bd86d599c4166423/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/zip/parsers.json) · [control verification](../../../../data/php/zip/verification.json) · [within-ecosystem ranking](../../../../data/php/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "content": "parsarium\n"
}
```

The pinned release reads the requested entry through PHP ZipArchive. Its listFiles method fails on PHP 8.5 because an associative callback array is interpreted as named arguments; this adapter verifies decompressed bytes only. Madnest is a fork of this package.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/chumper_zipper/README.md)

```sh
python3 parsarium.py build zip php chumper_zipper
python3 parsarium.py run zip php chumper_zipper controls/zip/hello.zip
```
