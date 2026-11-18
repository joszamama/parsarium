# imagesize — ASCII PNM / Rust

- **Pinned release:** `0.15.0`
- **Upstream:** [source repository](<https://github.com/Roughsketch/imagesize>) · [crates.io](<https://crates.io/crates/imagesize>)
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM header dimensions only; raster samples are not decoded
- **Underlying family:** imagesize PNM header reader
- **Local input API:** `blob_size(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/imagesize/0.15.0/imagesize/fn.blob_size.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/imagesize/README.md)

```sh
python3 parsarium.py build ascii_pnm rust imagesize
python3 parsarium.py run ascii_pnm rust imagesize controls/ascii_pnm/red-green.ppm
```
