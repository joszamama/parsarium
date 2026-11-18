# pdf_oxide — PDF / Rust

- **Pinned release:** `0.3.78`
- **Upstream:** [source repository](<https://github.com/yfedoseev/pdf_oxide>) · [crates.io](<https://crates.io/crates/pdf_oxide>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PDF page tree
- **Underlying family:** PDF Oxide parser
- **Local input API:** `PdfDocument::open(path).page_count()`
- **Documentation:** [API reference](<https://docs.rs/pdf_oxide/0.3.78/pdf_oxide/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdf_oxide/README.md)

```sh
python3 parsarium.py build pdf rust pdf_oxide
python3 parsarium.py run pdf rust pdf_oxide controls/pdf/one-page.pdf
```
