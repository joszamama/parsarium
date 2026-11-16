# pdf-extract — PDF / Rust

- **Pinned release:** `0.12.1`
- **License:** MIT
- **Parsed scope:** PDF text extraction
- **Underlying family:** lopdf
- **Local input API:** `extract_text(path)`
- **Documentation:** [API reference](<https://docs.rs/pdf-extract/0.12.1/pdf_extract/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "has_parsarium": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdf_extract/README.md)

```sh
python3 parsarium.py build pdf rust pdf_extract
python3 parsarium.py run pdf rust pdf_extract controls/pdf/one-page.pdf
```
