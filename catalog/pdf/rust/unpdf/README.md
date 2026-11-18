# unpdf — PDF / Rust

- **Pinned release:** `0.54.0`
- **Upstream:** [source repository](<https://github.com/iyulab/unpdf>) · [crates.io](<https://crates.io/crates/unpdf>)
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** unpdf parser
- **Local input API:** `parse_file(path).page_count()`
- **Documentation:** [API reference](<https://docs.rs/unpdf/0.54.0/unpdf/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/unpdf/README.md)

```sh
python3 parsarium.py build pdf rust unpdf
python3 parsarium.py run pdf rust unpdf controls/pdf/one-page.pdf
```
