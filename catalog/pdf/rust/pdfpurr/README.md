# pdfpurr — PDF / Rust

- **Pinned release:** `0.4.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PDF page tree
- **Underlying family:** pdfpurr parser
- **Local input API:** `Document::open(path).page_count()`
- **Documentation:** [API reference](<https://docs.rs/pdfpurr/0.4.0/pdfpurr/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdfpurr/README.md)

```sh
python3 parsarium.py build pdf rust pdfpurr
python3 parsarium.py run pdf rust pdfpurr controls/pdf/one-page.pdf
```
