# imageio-native-vips — SVG / Java

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** imageio-native-vips wrapper over libvips SVG decoder
- **Local input API:** `ImageIO.getImageReaders(ImageInputStream) selects ghosthack routing reader; ImageReader.read(0) delegates to libvips`
- **Documentation:** [API reference](<https://github.com/ghosthack/imageio-native#optional-backends>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
