# qpdf — PDF / C

- **Pinned release:** `12.4.2`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count
- **Underlying family:** qpdf C API over C++ PDF parser
- **Local input API:** `qpdf_init(); qpdf_read(qpdf_data, local filename, password); qpdf_get_num_pages()`
- **Documentation:** [API reference](<https://github.com/qpdf/qpdf/blob/v12.4.2/include/qpdf/qpdf-c.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

C translation unit linked with C++ linker, as official qpdf library documentation requires; shares qpdf engine with C++ PDF cell.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
