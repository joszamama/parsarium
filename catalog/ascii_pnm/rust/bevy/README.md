# bevy — ASCII PNM / Rust

- **Pinned release:** `0.20.1`
- **Upstream:** [source repository](<https://github.com/bevyengine/bevy>) · [crates.io](<https://crates.io/crates/bevy>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** P3 ASCII PPM expanded RGBA pixels
- **Underlying family:** Bevy re-export of bevy_image over image-rs PNM
- **Local input API:** `bevy::image::Image::from_buffer(&bytes, ImageType::Format(ImageFormat::Pnm), ...)`
- **Documentation:** [API reference](<https://docs.rs/bevy/0.20.1/bevy/image/struct.Image.html#method.from_buffer>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/bevy/README.md)

```sh
python3 parsarium.py build ascii_pnm rust bevy
python3 parsarium.py run ascii_pnm rust bevy controls/ascii_pnm/red-green.ppm
```
