# photocraft — ASCII PNM / Rust

- **Pinned release:** `0.1.2`
- **License:** GPL-3.0-or-later
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** photocraft PPM reader
- **Local input API:** `Image::read_ppm(&mut BufReader<Cursor<&[u8]>>)`
- **Documentation:** [API reference](<https://docs.rs/photocraft/0.1.2/photocraft/struct.Image.html#method.read_ppm>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
    255,
    0,
    0,
    0,
    255,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/photocraft/README.md)

```sh
python3 parsarium.py build ascii_pnm rust photocraft
python3 parsarium.py run ascii_pnm rust photocraft controls/ascii_pnm/red-green.ppm
```
