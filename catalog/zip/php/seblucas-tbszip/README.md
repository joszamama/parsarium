# seblucas/tbszip — ZIP / PHP

- **Pinned release:** `2.16.1`
- **License:** LGPL-2.1+
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** TbsZip custom PHP ZIP reader
- **Local input API:** `clsTbsZip::Open(local path); CdFileLst; FileRead`
- **Documentation:** [API reference](<https://github.com/seblucas/tbszip/blob/2c50bf309bb4431a24e206f164fdb4a2e6b10b7f/README.md>)
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

Parses central-directory records in PHP and uses zlib to decompress DEFLATE entries.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/seblucas_tbszip/README.md)

```sh
python3 parsarium.py build zip php seblucas_tbszip
python3 parsarium.py run zip php seblucas_tbszip controls/zip/hello.zip
```
