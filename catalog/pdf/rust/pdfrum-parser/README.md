# pdfrum-parser — PDF / Rust

- **Pinned release:** `0.5.3`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PDF xref and page tree
- **Underlying family:** pdfrum
- **Local input API:** `load(Arc::from(bytes), LoadOptions).page_count()`
- **Documentation:** [API reference](<https://docs.rs/pdfrum-parser/0.5.3/pdfrum_parser/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdfrum_parser/README.md)

```sh
python3 parsarium.py build pdf rust pdfrum_parser
python3 parsarium.py run pdf rust pdfrum_parser controls/pdf/one-page.pdf
```
