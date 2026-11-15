# png_pong — PNG / Rust

- **Pinned release:** `0.12.0`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
