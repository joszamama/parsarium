# C × PDF: verified parser ranking

7 verified third-party package paths; working goal 20, ceiling 30. Exact GitHub stars from primary upstream repositories are compared only within C × PDF. Stars proxy broad project interest, not PDF-specific adoption. Homebrew formula-name hits are discovery leads, not a popularity ranking. Poppler, MuPDF, Ghostscript, and PDFium have canonical non-GitHub upstreams and remain unranked.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [qpdf C API](https://github.com/qpdf/qpdf/blob/v12.4.2/include/qpdf/qpdf-c.h) | 12.4.2 | 5,582 | parsed PDF page count | qpdf C API over C++ PDF parser |
| 2 | [PDFio](https://www.msweet.org/pdfio/pdfio.html) | 1.6.5 | 361 | parsed PDF page count and first page object | PDFio PDF parser |
| 3 | [Vanilla.PDF](https://vanillapdf.readthedocs.io/en/stable/c_api.html) | 2.3.0 | 13 | parsed PDF page count and first page object | Vanilla.PDF C API over C++ PDF parser |
| unranked | [Poppler GLib](https://poppler.freedesktop.org/api/glib/PopplerDocument.html) | 26.11.0 | unknown | parsed PDF page count | Poppler PDF parser, GLib C frontend |
| unranked | [MuPDF](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | unknown | parsed PDF page count | MuPDF C document parser |
| unranked | [Ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | unknown | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| unranked | [PDFium](https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md) | 159.0.8152.0 | unknown | parsed PDF page count and first page object | PDFium PDF parser |

Apple Core Graphics is a verified macOS runtime API and is excluded from the third-party ranking. One lead remains unresolved. See `cell.json`, `registry-snapshot.json`, `parsers.json`, `standard.json`, and `verification.json` for limits and evidence.
