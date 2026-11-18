# pdf-inspector — PDF / Rust

- **Pinned release:** `1.25.2`
- **Upstream:** [source repository](<https://github.com/firecrawl/pdf-inspector>) · [crates.io](<https://crates.io/crates/pdf-inspector>)
- **License:** MIT
- **Parsed scope:** PDF page count and Info title
- **Underlying family:** lopdf
- **Local input API:** `process_pdf(path).page_count/title`
- **Documentation:** [API reference](<https://docs.rs/pdf-inspector/1.25.2/pdf_inspector/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdf_inspector/README.md)

```sh
python3 parsarium.py build pdf rust pdf_inspector
python3 parsarium.py run pdf rust pdf_inspector controls/pdf/one-page.pdf
```
