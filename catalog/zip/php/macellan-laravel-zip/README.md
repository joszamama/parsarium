# macellan/laravel-zip — ZIP / PHP

- **Pinned release:** `1.0.5`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Macellan fork of ZanySoft over PHP ZipArchive
- **Local input API:** `Macellan\Zip\Zip::open(local path); listFiles; extract`
- **Documentation:** [API reference](<https://github.com/macellan/laravel-zip/blob/0c40d22de710acb5e4da8620663fb336741cdc5d/README.md>)
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

A separate Composer package path with code lineage from ZanySoft Laravel ZIP; delegates parsing to PHP ZipArchive.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/macellan_laravel_zip/README.md)

```sh
python3 parsarium.py build zip php macellan_laravel_zip
python3 parsarium.py run zip php macellan_laravel_zip controls/zip/hello.zip
```
