# rusty-ppm — ASCII PNM / Rust

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM RGB pixels; compact spacing required by this release
- **Underlying family:** rusty-ppm reader
- **Local input API:** `ppm_reader::read_ppm(&control_path, control_filename)`
- **Documentation:** [API reference](<https://docs.rs/rusty-ppm/0.3.0/rusty_ppm/ppm_reader/fn.read_ppm.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green-compact.ppm`](../../../../controls/ascii_pnm/red-green-compact.ppm)

## Observed control result

```json
{
  "pixels": [
    [
      255,
      0,
      0
    ],
    [
      0,
      255,
      0
    ]
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/rusty_ppm/README.md)

```sh
python3 parsarium.py build ascii_pnm rust rusty_ppm
python3 parsarium.py run ascii_pnm rust rusty_ppm controls/ascii_pnm/red-green-compact.ppm
```
