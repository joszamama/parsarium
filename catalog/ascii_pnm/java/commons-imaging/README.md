# commons-imaging — ASCII PNM / Java

- **Pinned release:** `1.0.0-alpha6`
- **Upstream:** [source repository](<https://gitbox.apache.org/repos/asf?p=commons-imaging.git>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.commons/commons-imaging>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** Apache Commons Imaging PNM decoder
- **Local input API:** `Imaging.getBufferedImage(File)`
- **Documentation:** [API reference](<https://commons.apache.org/proper/commons-imaging/formatsupport.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/commons_imaging/README.md)

```sh
python3 parsarium.py build ascii_pnm java commons_imaging
python3 parsarium.py run ascii_pnm java commons_imaging controls/ascii_pnm/red-green.ppm
```
