# quarkus-fs-util — ZIP / Java

- **Pinned release:** `1.4.2`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Quarkus read-only ZIP filesystem parser
- **Local input API:** `ZipUtils.openReadOnly(path); Files.readAllBytes(zipFs.getPath(name))`
- **Documentation:** [API reference](<https://github.com/quarkusio/quarkus-fs-util>)
- **Catalog evidence:** [parser record](../../../../data/java/zip/parsers.json) · [control verification](../../../../data/java/zip/verification.json) · [within-ecosystem ranking](../../../../data/java/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/java/quarkus_fs_util/README.md)

```sh
python3 parsarium.py build zip java quarkus_fs_util
python3 parsarium.py run zip java quarkus_fs_util controls/zip/hello.zip
```
