# rigidity-io — ASCII PLY / Rust

- **Pinned release:** `0.2.0`
- **License:** AGPL-3.0-only
- **Parsed scope:** ASCII PLY vertex cloud; faces not interpreted
- **Underlying family:** rigidity-io PLY reader
- **Local input API:** `read_ply(path)`
- **Documentation:** [API reference](<https://docs.rs/rigidity-io/0.2.0/rigidity_io/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
