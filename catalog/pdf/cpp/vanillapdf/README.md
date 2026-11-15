# vanillapdf — PDF / C++

- **Pinned release:** `2.3.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count and first page object
- **Underlying family:** Vanilla.PDF C API over C++ PDF parser
- **Local input API:** `Document_Open(local filename); Document_GetCatalog(); Catalog_GetPages(); PageTree_GetPageCount() and PageTree_GetPage(1)`
- **Documentation:** [API reference](<https://vanillapdf.readthedocs.io/en/stable/c_api.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Official publisher C ABI backed by its native C++ parser. C and C++ call sites share the same v2.3.0 engine and are one package path per ecosystem; the C++ call site uses the documented C API, not a separate C++ API.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
