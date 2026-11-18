# jai-imageio-core — ASCII PNM / Java

- **Pinned release:** `1.4.0`
- **Upstream:** [source repository](<https://github.com/jai-imageio/jai-imageio-core>) · [Maven Central](<https://central.sonatype.com/artifact/com.github.jai-imageio/jai-imageio-core>)
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** JAI ImageIO PNM plugin
- **Local input API:** `JAI PNM ImageReader.setInput(ImageInputStream).read(0)`
- **Documentation:** [API reference](<https://github.com/jai-imageio/jai-imageio-core#jai-imageio-core-standalone>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/jai_imageio_core/README.md)

```sh
python3 parsarium.py build ascii_pnm java jai_imageio_core
python3 parsarium.py run ascii_pnm java jai_imageio_core controls/ascii_pnm/red-green.ppm
```
