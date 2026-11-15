# pdfwriter — PDF / C++

- **Pinned release:** `4.6.2`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count
- **Underlying family:** PDF-Writer (PDFHummus) PDF parser
- **Local input API:** `InputFile::OpenFile(local path), PDFParser::StartPDFParsing(file.GetInputStream()), PDFParser::GetPagesCount()`
- **Documentation:** [API reference](<https://github.com/galkahana/PDF-Writer/wiki/PDF-Parsing>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Native C++ PDFParser in the PDF-Writer package; source-built from pinned v4.6.2 release with bundled Aesgm and system Zlib/FreeType. DCT, TIFF, and PNG integrations are disabled for this simple PDF control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
