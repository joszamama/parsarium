# img-parts — PNG / Rust

- **Pinned release:** `0.4.2`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PNG chunk structure and IHDR dimensions
- **Underlying family:** img-parts PNG chunk reader
- **Local input API:** `png::Png::from_bytes(Bytes)`
- **Documentation:** [API reference](<https://docs.rs/img-parts/0.4.2/img_parts/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "chunks": 3
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
