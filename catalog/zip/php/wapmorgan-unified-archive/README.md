# wapmorgan/unified-archive — ZIP / PHP

- **Pinned release:** `1.3.1`
- **Upstream:** [source repository](<https://github.com/wapmorgan/UnifiedArchive>) · [Packagist](<https://packagist.org/packages/wapmorgan/unified-archive>)
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** UnifiedArchive ZIP driver over PHP ZipArchive
- **Local input API:** `UnifiedArchive::open(local path); getFiles; getFileContent`
- **Documentation:** [API reference](<https://github.com/wapmorgan/UnifiedArchive/blob/2097cdf0995f4a576773d66803af4245ed55636e/docs/API.md>)
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

Observed driver is wapmorgan\UnifiedArchive\Drivers\Zip, which uses bundled ZipArchive/libzip; package also bundles PclZip as an alternative backend.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/wapmorgan_unified_archive/README.md)

```sh
python3 parsarium.py build zip php wapmorgan_unified_archive
python3 parsarium.py run zip php wapmorgan_unified_archive controls/zip/hello.zip
```
