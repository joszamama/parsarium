# C++ × PDF: verified parser ranking

6 verified third-party package paths; working goal 20, ceiling 30. Exact GitHub stars of each primary upstream repository are compared only within C++. Stars proxy broad project interest, not PDF-specific adoption. Homebrew formula search names are discovery leads, not a popularity ranking. Poppler, MuPDF, and Ghostscript have canonical non-GitHub upstreams and remain unranked.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [qpdf](https://github.com/qpdf/qpdf/blob/v12.4.2/examples/pdf-parse-content.cc) | 12.4.2 | 5,582 | parsed PDF page count | qpdf C++ PDF parser |
| 2 | [PoDoFo](https://github.com/podofo/podofo/blob/1.1.2/src/podofo/main/PdfMemDocument.h) | 1.1.2 | 616 | parsed PDF page count | PoDoFo PDF parser |
| 3 | [PDFio](https://www.msweet.org/pdfio/pdfio.html) | 1.6.5 | 361 | parsed PDF page count and first page object | PDFio PDF parser |
| unranked | [Poppler C++](https://poppler.freedesktop.org/api/cpp/classpoppler_1_1document.html) | 26.11.0 | unknown | parsed PDF page count | Poppler PDF parser, C++ frontend |
| unranked | [MuPDF](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | unknown | parsed PDF page count | MuPDF C document parser |
| unranked | [Ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | unknown | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |

Five leads remain unresolved. See `cell.json`, `registry-snapshot.json`, `parsers.json`, and `verification.json` for limits and evidence.
