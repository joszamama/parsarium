# zanysoft/laravel-zip — ZIP / PHP

- **Pinned release:** `3.1.0`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** ZanySoft ZIP wrapper over PHP ZipArchive
- **Local input API:** `ZanySoft\Zip\Zip::open(local path); listFiles; extract`
- **Documentation:** [API reference](<https://github.com/zanysoft/laravel-zip/blob/ee2a4f44a0236bab8e223c0eb8c4c8b6c739cb9b/README.md>)
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

Opens the local ZIP with PHP ZipArchive and extracts the selected entry.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/zanysoft_laravel_zip/README.md)

```sh
python3 parsarium.py build zip php zanysoft_laravel_zip
python3 parsarium.py run zip php zanysoft_laravel_zip controls/zip/hello.zip
```
