# vipsoft/unzip — ZIP / PHP

- **Pinned release:** `1.3`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** VIPSoft wrapper over PHP ZipArchive
- **Local input API:** `VIPSoft\Unzip\Unzip::extract(local path, destination)`
- **Documentation:** [API reference](<https://github.com/vipsoft/Unzip/blob/090712dc65d0d77842f077d0a768fc7c852d4624/README.md>)
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

Distinct package API that delegates ZIP parsing to bundled ZipArchive/libzip.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/vipsoft_unzip/README.md)

```sh
python3 parsarium.py build zip php vipsoft_unzip
python3 parsarium.py run zip php vipsoft_unzip controls/zip/hello.zip
```
