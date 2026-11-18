# league/flysystem-ziparchive — ZIP / PHP

- **Pinned release:** `3.31.0`
- **Upstream:** [source repository](<https://github.com/thephpleague/flysystem-ziparchive>) · [Packagist](<https://packagist.org/packages/league/flysystem-ziparchive>)
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Flysystem ZIP adapter over PHP ZipArchive
- **Local input API:** `FilesystemZipArchiveProvider(local path); ZipArchiveAdapter::listContents/read`
- **Documentation:** [API reference](<https://github.com/thephpleague/flysystem-ziparchive/blob/ab6f9041b61ef517bc3e81891a4969181a39c17a/ZipArchiveAdapter.php>)
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

Distinct Flysystem adapter package API; ZIP parsing uses bundled ZipArchive/libzip.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/league_flysystem_ziparchive/README.md)

```sh
python3 parsarium.py build zip php league_flysystem_ziparchive
python3 parsarium.py run zip php league_flysystem_ziparchive controls/zip/hello.zip
```
