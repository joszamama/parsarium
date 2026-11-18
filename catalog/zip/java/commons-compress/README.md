# commons-compress — ZIP / Java

- **Pinned release:** `1.28.0`
- **Upstream:** [source repository](<https://gitbox.apache.org/repos/asf?p=commons-compress.git>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.commons/commons-compress>)
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Apache Commons Compress ZIP parser
- **Local input API:** `org.apache.commons.compress.archivers.zip.ZipFile.builder().setPath(path).get(); getEntry/getInputStream`
- **Documentation:** [API reference](<https://commons.apache.org/proper/commons-compress/apidocs/org/apache/commons/compress/archivers/zip/ZipFile.html>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/commons_compress/README.md)

```sh
python3 parsarium.py build zip java commons_compress
python3 parsarium.py run zip java commons_compress controls/zip/hello.zip
```
