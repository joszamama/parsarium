# roka-qr — ASCII PNM / Rust

- **Pinned release:** `0.1.1`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** P1 ASCII PBM QR image and payload
- **Underlying family:** roka-qr P1 bitmap reader plus QR decoder
- **Local input API:** `Reader::from_pbm(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/roka-qr/0.1.1/roka_qr/struct.Reader.html#method.from_pbm>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/qr-p1.pbm`](../../../../controls/ascii_pnm/qr-p1.pbm)

## Observed control result

```json
{
  "size": 25,
  "payload": "Parsarium P1 control"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
