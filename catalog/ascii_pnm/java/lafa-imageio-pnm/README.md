# lafa-imageio-pnm — ASCII PNM / Java

- **Pinned release:** `1.0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII P3 PPM dimensions and red/green pixels; isolated fork classpath
- **Underlying family:** Lafa fork of TwelveMonkeys PNM ImageIO plugin
- **Local input API:** `ImageIO.getImageReaders(ImageInputStream local file); PNMImageReader.read(0)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/imageio/imageio-pnm/1.0/imageio-pnm-1.0.pom>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "reader": "com.twelvemonkeys.imageio.plugins.pnm.PNMImageReader",
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
