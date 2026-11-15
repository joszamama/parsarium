# imageio-native-vips — ASCII PNM / Java

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** imageio-native-vips wrapper over libvips Netpbm decoder
- **Local input API:** `ImageIO.getImageReaders(ImageInputStream local file) selects ghosthack routing reader; read(0) delegates to libvips`
- **Documentation:** [API reference](<https://github.com/ghosthack/imageio-native#optional-backends>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
