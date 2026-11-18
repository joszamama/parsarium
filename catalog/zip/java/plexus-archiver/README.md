# plexus-archiver — ZIP / Java

- **Pinned release:** `4.15.0`
- **Upstream:** [source repository](<https://github.com/codehaus-plexus/plexus-archiver>) · [Maven Central](<https://central.sonatype.com/artifact/org.codehaus.plexus/plexus-archiver>)
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Plexus Archiver wrapper over Commons Compress
- **Local input API:** `new ZipUnArchiver(file).setDestDirectory(dir); extract()`
- **Documentation:** [API reference](<https://codehaus-plexus.github.io/plexus-archiver/apidocs/org/codehaus/plexus/archiver/zip/ZipUnArchiver.html>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/plexus_archiver/README.md)

```sh
python3 parsarium.py build zip java plexus_archiver
python3 parsarium.py run zip java plexus_archiver controls/zip/hello.zip
```
