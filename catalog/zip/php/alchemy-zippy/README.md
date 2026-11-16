# alchemy/zippy — ZIP / PHP

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Alchemy Zippy wrapper over PHP ZipArchive
- **Local input API:** `ZipExtensionAdapter::newInstance()->open(local path); getMembers; extract`
- **Documentation:** [API reference](<https://github.com/alchemy-fr/Zippy/blob/3546ecd8ad5a1a1efb13315a5ea8ff1c7a1d5ef8/src/Zippy.php>)
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

The adapter selects Zippy’s ZipExtensionAdapter explicitly; ZIP parsing uses bundled ZipArchive/libzip, not an external command.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/alchemy_zippy/README.md)

```sh
python3 parsarium.py build zip php alchemy_zippy
python3 parsarium.py run zip php alchemy_zippy controls/zip/hello.zip
```
