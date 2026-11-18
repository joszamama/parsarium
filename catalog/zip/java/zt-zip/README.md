# zt-zip — ZIP / Java

- **Pinned release:** `1.18.2`
- **Upstream:** [source repository](<https://github.com/zeroturnaround/zt-zip>) · [Maven Central](<https://central.sonatype.com/artifact/org.zeroturnaround/zt-zip>)
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** zt-zip wrapper over JDK ZipFile
- **Local input API:** `org.zeroturnaround.zip.ZipUtil.iterate(file, ZipEntryCallback)`
- **Documentation:** [API reference](<https://github.com/zeroturnaround/zt-zip>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/zt_zip/README.md)

```sh
python3 parsarium.py build zip java zt_zip
python3 parsarium.py run zip java zt_zip controls/zip/hello.zip
```
