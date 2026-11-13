# C++ × PDF: verified parser ranking

19 verified third-party package paths; working goal 20, ceiling 30. Exact GitHub stars of each primary upstream repository are compared only within C++. Stars proxy broad project interest, not PDF-specific adoption. Homebrew formula search names are discovery leads, not a popularity ranking. Poppler, MuPDF, Ghostscript, PDFium, Qt PDF, Xpdf, and GraphicsMagick have canonical non-GitHub upstreams and remain unranked.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | rendered PDF page and dimensions | ImageMagick PDF coder + Ghostscript |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.pdfload.html) | 8.18.7 | 11,801 | PDF page count and first page dimensions | vips-poppler module over Poppler |
| 3 | [qpdf](https://github.com/qpdf/qpdf/blob/v12.4.2/examples/pdf-parse-content.cc) | 12.4.2 | 5,582 | parsed PDF page count | qpdf C++ PDF parser |
| 4 | [PDF4QT](https://github.com/JakubMelka/PDF4QT/blob/v1.6.0.0/Pdf4QtLibCore/sources/pdfdocumentreader.h) | 1.6.0.0 | 1,515 | parsed PDF page count | PDF4QT PDF engine |
| 5 | [PDF-Writer](https://github.com/galkahana/PDF-Writer/wiki/PDF-Parsing) | 4.6.2 | 1,029 | parsed PDF page count | PDF-Writer (PDFHummus) PDF parser |
| 6 | [PoDoFo](https://github.com/podofo/podofo/blob/1.1.2/src/podofo/main/PdfMemDocument.h) | 1.1.2 | 616 | parsed PDF page count | PoDoFo PDF parser |
| 7 | [PDFio](https://www.msweet.org/pdfio/pdfio.html) | 1.6.5 | 361 | parsed PDF page count and first page object | PDFio PDF parser |
| 8 | [Docling Parse](https://github.com/docling-project/docling-parse/blob/v7.25.0/src/parse/pdf_decoders/document.h) | 7.25.0 | 347 | parsed PDF page count | qpdf engine via Docling Parse |
| 9 | [pdfmm](https://github.com/pdfmm/pdfmm/blob/v0.10.0/src/pdfmm/base/PdfMemDocument.h) | 0.10.0 | 62 | parsed PDF page count | pdfmm, fork of PoDoFo |
| 10 | [Vanilla.PDF](https://vanillapdf.readthedocs.io/en/stable/c_api.html) | 2.3.0 | 13 | parsed PDF page count and first page object | Vanilla.PDF C API over C++ PDF parser |
| 11 | [Aspose.PDF FOSS](https://github.com/aspose-pdf-foss/Aspose.PDF-FOSS-for-Cpp/blob/v1.0.1/README.md) | 1.0.1 | 2 | parsed PDF page count | Aspose.PDF FOSS native C++ parser |
| 12 | [tspdf](https://github.com/be-lang/tspdf/blob/v0.5.1/docs/library.md) | 0.5.1 | 0 | parsed PDF page count and first page | tspdf pure C11 PDF parser |
| unranked | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | unknown | rendered PDF page and dimensions | GraphicsMagick PDF coder + Ghostscript |
| unranked | [Poppler C++](https://poppler.freedesktop.org/api/cpp/classpoppler_1_1document.html) | 26.11.0 | unknown | parsed PDF page count | Poppler PDF parser, C++ frontend |
| unranked | [MuPDF](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | unknown | parsed PDF page count | MuPDF C document parser |
| unranked | [Ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | unknown | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| unranked | [Qt PDF](https://doc.qt.io/qt-6/qpdfdocument.html) | 6.11.2 | unknown | parsed PDF page count | PDFium engine via Qt PDF |
| unranked | [Xpdf](https://dl.xpdfreader.com/xpdf-4.06.tar.gz) | 4.06 | unknown | parsed PDF page count | Xpdf PDF parser |
| unranked | [PDFium](https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md) | 159.0.8152.0 | unknown | parsed PDF page count and first page object | PDFium PDF parser |

One cpdflib lead remains unresolved because its tagged C/C++ binary release has a noncommercial license; poppler-qt6 was excluded as a duplicate Poppler package frontend. See `cell.json`, `registry-snapshot.json`, `parsers.json`, and `verification.json` for limits and evidence.

tspdf had zero primary GitHub stars at observation time; listing it records a verified reader, not proven adoption.

Both Magick paths use Ghostscript for PDF interpretation in the recorded build and do not add independent PDF syntax engines.

libvips loads PDF through its Poppler module in this pinned installation and shares that underlying parser with the Poppler path.
