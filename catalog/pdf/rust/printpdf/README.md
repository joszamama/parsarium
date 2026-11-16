# printpdf — PDF / Rust

- **Pinned release:** `0.12.9`
- **License:** MIT
- **Parsed scope:** PDF page model
- **Underlying family:** lopdf
- **Local input API:** `PdfDocument::parse(&bytes, options, warnings).pages`
- **Documentation:** [API reference](<https://docs.rs/printpdf/0.12.9/printpdf/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/printpdf/README.md)

```sh
python3 parsarium.py build pdf rust printpdf
python3 parsarium.py run pdf rust printpdf controls/pdf/one-page.pdf
```
