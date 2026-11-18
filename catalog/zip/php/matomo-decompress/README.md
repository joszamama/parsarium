# matomo/decompress — ZIP / PHP

- **Pinned release:** `3.0.0`
- **Upstream:** [source repository](<https://github.com/matomo-org/component-decompress>) · [Packagist](<https://packagist.org/packages/matomo/decompress>)
- **License:** LGPL-3.0
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Matomo extractor over PHP ZipArchive
- **Local input API:** `Matomo\Decompress\ZipArchive(local ZIP path); extract(destination)`
- **Documentation:** [API reference](<https://github.com/matomo-org/component-decompress/blob/3e96938cd11f90e5e4bcc38c78264c86a63f41bb/README.md>)
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

The explicit ZipArchive backend parses the local archive and returns per-entry metadata; the package also offers a bundled PclZip backend.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/matomo_decompress/README.md)

```sh
python3 parsarium.py build zip php matomo_decompress
python3 parsarium.py run zip php matomo_decompress controls/zip/hello.zip
```
