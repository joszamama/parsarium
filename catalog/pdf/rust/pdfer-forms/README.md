# pdfer_forms — PDF / Rust

- **Pinned release:** `0.3.4`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PDF page handles
- **Underlying family:** lopdf
- **Local input API:** `PdfReaderCompat::load(path).pages()`
- **Documentation:** [API reference](<https://docs.rs/pdfer_forms/0.3.4/pdfer_forms/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdfer_forms/README.md)

```sh
python3 parsarium.py build pdf rust pdfer_forms
python3 parsarium.py run pdf rust pdfer_forms controls/pdf/one-page.pdf
```
