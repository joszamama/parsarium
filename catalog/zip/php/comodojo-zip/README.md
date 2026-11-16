# comodojo/zip — ZIP / PHP

- **Pinned release:** `3.1.1`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Comodojo wrapper over PHP ZipArchive
- **Local input API:** `Comodojo\Zip\Zip::open(local path); listFiles; extract`
- **Documentation:** [API reference](<https://github.com/comodojo/zip/blob/22e11bda2ab8e1057cf4d1a50a98ab22f9e38e34/src/Comodojo/Zip/Zip.php>)
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

Distinct package API backed by bundled ZipArchive/libzip; emits PHP 8.5 deprecation notices during the valid control.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/comodojo_zip/README.md)

```sh
python3 parsarium.py build zip php comodojo_zip
python3 parsarium.py run zip php comodojo_zip controls/zip/hello.zip
```
