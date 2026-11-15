# lopdf — PDF / Rust

- **Pinned release:** `0.47.0`
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** lopdf
- **Local input API:** `Document::load(path).get_pages()`
- **Documentation:** [API reference](<https://docs.rs/lopdf/0.47.0/lopdf/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/lopdf/README.md)

```sh
python3 parsarium.py build pdf rust lopdf
python3 parsarium.py run pdf rust lopdf controls/pdf/one-page.pdf
```
