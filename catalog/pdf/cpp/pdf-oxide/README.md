# pdf_oxide — PDF / C++

- **Pinned release:** `0.3.78`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** parsed PDF page count
- **Underlying family:** pdf_oxide Rust PDF parser via C ABI
- **Local input API:** `pdf_oxide::Document::open(local file path); page_count()`
- **Documentation:** [API reference](<https://github.com/yfedoseev/pdf_oxide/blob/v0.3.78/cpp/include/pdf_oxide/pdf_oxide.hpp>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

The C++17 RAII facade calls the tagged pdf_oxide C ABI, which enters the same Rust 0.3.78 PDF engine as the selected Rust package path. This is a distinct C++ package API but not an independent PDF syntax parser. The C ABI route was examined separately and was not selected for the C/PDF top ten.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/pdf_oxide/README.md)

```sh
python3 parsarium.py build pdf cpp pdf_oxide
python3 parsarium.py run pdf cpp pdf_oxide controls/pdf/one-page.pdf
```

**Coverage limit:** AFL++ pcguard guards cover the whole pdf_oxide crate, not only its syntax modules: stable rustc's sancov-module pass takes no source allowlist. Dependencies and the C++ harness are uninstrumented. The AFL++ target is one-shot /work/replay @@.
