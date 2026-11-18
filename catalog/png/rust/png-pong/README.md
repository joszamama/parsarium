# png_pong — PNG / Rust

- **Pinned release:** `0.12.0`
- **Upstream:** [source repository](<https://github.com/AldaronLau/png_pong>) · [crates.io](<https://crates.io/crates/png_pong>)
- **License:** (Apache-2.0 OR BSL-1.0 OR MIT) AND Zlib
- **Parsed scope:** Decoded PNG frame dimensions
- **Underlying family:** png_pong decoder
- **Local input API:** `Decoder::new(BufRead).into_steps()`
- **Documentation:** [API reference](<https://docs.rs/png_pong/0.12.0/png_pong/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/rust/png_pong/README.md)

```sh
python3 parsarium.py build png rust png_pong
python3 parsarium.py run png rust png_pong controls/png/red-green.png
```
