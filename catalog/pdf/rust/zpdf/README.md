# zpdf — PDF / Rust

- **Pinned release:** `0.18.0`
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** zpdf
- **Local input API:** `PdfDocument::open(bytes).page_count()`
- **Documentation:** [API reference](<https://docs.rs/zpdf/0.18.0/zpdf/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/zpdf/README.md)

```sh
python3 parsarium.py build pdf rust zpdf
python3 parsarium.py run pdf rust zpdf controls/pdf/one-page.pdf
```
