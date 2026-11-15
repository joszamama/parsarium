# tspdf — PDF / C++

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** PDF document page count and first parsed page
- **Underlying family:** tspdf pure C11 PDF parser
- **Local input API:** `tspdf_reader_open_file(local filename, error); tspdf_reader_page_count(); tspdf_reader_get_page(0)`
- **Documentation:** [API reference](<https://github.com/be-lang/tspdf/blob/v0.5.1/docs/library.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

The same source library and parser engine is used by the C and C++17 adapters; counted once per ecosystem, not as separate syntax engines. Its zero-star GitHub metric is recorded without claiming broad adoption.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
