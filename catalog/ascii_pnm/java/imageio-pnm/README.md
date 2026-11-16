# imageio-pnm — ASCII PNM / Java

- **Pinned release:** `3.15.3`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** TwelveMonkeys PNM ImageIO plugin
- **Local input API:** `TwelveMonkeys PNM ImageReader.setInput(ImageInputStream).read(0)`
- **Documentation:** [API reference](<https://github.com/haraldk/TwelveMonkeys#file-formats-supported>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/imageio_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm java imageio_pnm
python3 parsarium.py run ascii_pnm java imageio_pnm controls/ascii_pnm/red-green.ppm
```
