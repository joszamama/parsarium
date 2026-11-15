# gufo-png — PNG / Rust

- **Pinned release:** `0.5.0`
- **License:** MPL-2.0 OR LGPL-2.1-or-later
- **Parsed scope:** PNG tEXt Title metadata
- **Underlying family:** gufo-png chunk reader
- **Local input API:** `Png::new(Vec<u8>).chunks().text()`
- **Documentation:** [API reference](<https://docs.rs/gufo-png/0.5.0/gufo_png/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green-title.png`](../../../../controls/png/red-green-title.png)

## Observed control result

```json
{
  "key": "Title",
  "value": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
