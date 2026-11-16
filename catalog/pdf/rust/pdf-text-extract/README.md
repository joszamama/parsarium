# pdf-text-extract — PDF / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** PDF xref, catalog, and page count
- **Underlying family:** pdf-text-extract parser
- **Local input API:** `Document::parse(&bytes).page_count()`
- **Documentation:** [API reference](<https://docs.rs/pdf-text-extract/0.2.0/pdf_text_extract/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdf_text_extract/README.md)

```sh
python3 parsarium.py build pdf rust pdf_text_extract
python3 parsarium.py run pdf rust pdf_text_extract controls/pdf/one-page.pdf
```
