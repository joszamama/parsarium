# unpdf — PDF / C

- **Pinned release:** `0.54.0`
- **License:** MIT
- **Parsed scope:** parsed PDF page-tree count through C ABI
- **Underlying family:** unpdf Rust PDF parser via C ABI
- **Local input API:** `unpdf_parse_file(local path) returns document handle; unpdf_page_count(document) returns PDF page-tree count; unpdf_free_document(handle)`
- **Documentation:** [API reference](<https://github.com/iyulab/unpdf/blob/v0.54.0/src/ffi.rs>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

The pinned Rust crate publishes a C ABI with local-file parsing and page-count calls. This is the same underlying parser as the verified Rust unpdf path; C adoption is not inferred from Rust crate downloads.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
