# zenpng — PNG / Rust

- **Pinned release:** `0.1.4`
- **Upstream:** [source repository](<https://github.com/imazen/zenpng>) · [crates.io](<https://crates.io/crates/zenpng>)
- **License:** AGPL-3.0-only OR LicenseRef-Imazen-Commercial
- **Parsed scope:** Decoded PNG dimensions
- **Underlying family:** zenpng engine
- **Local input API:** `decode(&[u8], &PngDecodeConfig, &Unstoppable)`
- **Documentation:** [API reference](<https://docs.rs/zenpng/0.1.4/zenpng/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/zenpng/README.md)

```sh
python3 parsarium.py build png rust zenpng
python3 parsarium.py run png rust zenpng controls/png/red-green.png
```
