# commons-imaging — PNG / Java

- **Pinned release:** `1.0.0-alpha6`
- **Upstream:** [source repository](<https://gitbox.apache.org/repos/asf?p=commons-imaging.git>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.commons/commons-imaging>)
- **License:** Apache-2.0
- **Parsed scope:** RGBA pixels
- **Underlying family:** Apache Commons Imaging PNG decoder
- **Local input API:** `Imaging.getBufferedImage(File)`
- **Documentation:** [API reference](<https://javadoc.io/static/org.apache.commons/commons-imaging/1.0.0-alpha6/org/apache/commons/imaging/Imaging.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/commons_imaging/README.md)

```sh
python3 parsarium.py build png java commons_imaging
python3 parsarium.py run png java commons_imaging controls/png/red-green.png
```
