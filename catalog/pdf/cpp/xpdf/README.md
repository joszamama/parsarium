# xpdf — PDF / C++

- **Pinned release:** `4.06`
- **License:** GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** PDF document page count
- **Underlying family:** Xpdf PDF parser
- **Local input API:** `PDFDoc(char* local UTF-8 filename) after GlobalParams initialization; isOk(); getNumPages(), defined in xpdf/PDFDoc.h and used by xpdf/pdfinfo.cc in the pinned source archive`
- **Documentation:** [API reference](<https://dl.xpdfreader.com/xpdf-4.06.tar.gz>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Xpdf 4.06 source publishes a CMake xpdf_objs object library containing PDFDoc; the verifier archives it and links its goo and fofi libraries for a direct C++17 adapter. There is no installed public libxpdf artifact or stable ABI claim. Poppler descends from older Xpdf code, but this is the independently maintained Xpdf 4.06 parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
