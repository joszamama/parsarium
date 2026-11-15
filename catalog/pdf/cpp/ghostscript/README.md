# ghostscript — PDF / C++

- **Pinned release:** `10.08.0`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PDF interpreter NumPages metadata
- **Underlying family:** Ghostscript PDF interpreter
- **Local input API:** `gsapi_run_string on a local file path using Ghostscript PDF interpreter .PDFInit, .PDFFile, .PDFInfo /NumPages; C API called from C++17`
- **Documentation:** [API reference](<https://ghostscript.readthedocs.io/en/master/Language.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct Ghostscript C API call from C++17; PDF interpreter is a distinct engine from Poppler, PoDoFo, qpdf, and MuPDF. Source archive is GhostPDL, which contains Ghostscript. Canonical upstream is Ghostscript Git; GitHub mirrors are not used for popularity.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
