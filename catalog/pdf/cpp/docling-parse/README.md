# docling_parse — PDF / C++

- **Pinned release:** `7.25.0`
- **License:** MIT
- **Parsed scope:** PDF document page count
- **Underlying family:** qpdf engine via Docling Parse
- **Local input API:** `pdflib::pdf_decoder<pdflib::DOCUMENT>::process_document_from_file(std::string& local filename, std::optional<std::string>& password); get_number_of_pages()`
- **Documentation:** [API reference](<https://github.com/docling-project/docling-parse/blob/v7.25.0/src/parse/pdf_decoders/document.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Docling Parse 7.25.0 exposes a C++20 local-file decoder over bundled qpdf. It is a distinct source package and API but shares qpdf as the PDF syntax engine. A pinned-source CMake target builds the adapter with pinned LLVM and bundled dependency tags; the recorded patch only adds the adapter target and propagates LLVM into the qpdf subbuild. The source does not publish a separately installed stable C++ ABI.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
