# pdf — PDF / Rust

- **Pinned release:** `0.10.0`
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** pdf-rs parser
- **Local input API:** `FileOptions::cached().open(path).num_pages()`
- **Documentation:** [API reference](<https://docs.rs/pdf/0.10.0/pdf/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdf/README.md)

```sh
python3 parsarium.py build pdf rust pdf
python3 parsarium.py run pdf rust pdf controls/pdf/one-page.pdf
```
