# CPP × PDF: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub stars of primary upstream repository.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [imagemagick](https://imagemagick.org/magick++/) | 7.1.2-35 | 17,852 | Rendered PDF page sequence and first page dimensions | ImageMagick PDF coder + Ghostscript PDF interpreter |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.pdfload.html) | 8.18.7 | 11,801 | PDF page count and first page dimensions from PDF loader header | libvips vips-poppler module over Poppler PDF parser |
| 3 | [qpdf](https://github.com/qpdf/qpdf/blob/v12.4.2/examples/pdf-parse-content.cc) | 12.4.2 | 5,582 | PDF document page count | qpdf C++ PDF parser |
| 4 | [pdf4qt](https://github.com/JakubMelka/PDF4QT/blob/v1.6.0.0/Pdf4QtLibCore/sources/pdfdocumentreader.h) | 1.6.0.0 | 1,515 | PDF document page count | PDF4QT PDF engine |
| 5 | [pdf_oxide](https://github.com/yfedoseev/pdf_oxide/blob/v0.3.78/cpp/include/pdf_oxide/pdf_oxide.hpp) | 0.3.78 | 1,186 | parsed PDF page count | pdf_oxide Rust PDF parser via C ABI |
| 6 | [pdfwriter](https://github.com/galkahana/PDF-Writer/wiki/PDF-Parsing) | 4.6.2 | 1,029 | PDF document page count | PDF-Writer (PDFHummus) PDF parser |
| 7 | [podofo](https://github.com/podofo/podofo/blob/1.1.2/src/podofo/main/PdfMemDocument.h) | 1.1.2 | 616 | PDF document page count | PoDoFo PDF parser |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | [Debian source installed count](https://sources.debian.org/src/ghostscript/) | 165,837 | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| 2 | [poppler](https://poppler.freedesktop.org/api/cpp/classpoppler_1_1document.html) | 26.11.0 | [Debian source installed count](https://sources.debian.org/src/poppler/) | 141,779 | PDF document page count | Poppler PDF parser, C++ frontend |
| 3 | [mupdf](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | [Debian source installed count](https://sources.debian.org/src/mupdf/) | 20,144 | PDF document page count | MuPDF C document parser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
