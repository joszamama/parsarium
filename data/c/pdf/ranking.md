# C × PDF: verified parser ranking

11 verified third-party package paths; working goal 20, ceiling 30. Exact GitHub stars from primary upstream repositories are compared only within C × PDF. Stars proxy broad project interest, not PDF-specific adoption. Homebrew formula-name hits are discovery leads, not a popularity ranking. Poppler, MuPDF, Ghostscript, PDFium, and GraphicsMagick have canonical non-GitHub upstreams and remain unranked.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | rendered PDF page and dimensions | ImageMagick PDF coder + Ghostscript |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.pdfload.html) | 8.18.7 | 11,801 | PDF page count and first page dimensions | vips-poppler module over Poppler |
| 3 | [qpdf C API](https://github.com/qpdf/qpdf/blob/v12.4.2/include/qpdf/qpdf-c.h) | 12.4.2 | 5,582 | parsed PDF page count | qpdf C API over C++ PDF parser |
| 4 | [PDFio](https://www.msweet.org/pdfio/pdfio.html) | 1.6.5 | 361 | parsed PDF page count and first page object | PDFio PDF parser |
| 5 | [Vanilla.PDF](https://vanillapdf.readthedocs.io/en/stable/c_api.html) | 2.3.0 | 13 | parsed PDF page count and first page object | Vanilla.PDF C API over C++ PDF parser |
| 6 | [tspdf](https://github.com/be-lang/tspdf/blob/v0.5.1/docs/library.md) | 0.5.1 | 0 | parsed PDF page count and first page | tspdf pure C11 PDF parser |
| unranked | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | unknown | rendered PDF page and dimensions | GraphicsMagick PDF coder + Ghostscript |
| unranked | [Poppler GLib](https://poppler.freedesktop.org/api/glib/PopplerDocument.html) | 26.11.0 | unknown | parsed PDF page count | Poppler PDF parser, GLib C frontend |
| unranked | [MuPDF](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | unknown | parsed PDF page count | MuPDF C document parser |
| unranked | [Ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | unknown | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| unranked | [PDFium](https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md) | 159.0.8152.0 | unknown | parsed PDF page count and first page object | PDFium PDF parser |

Apple Core Graphics is a verified macOS runtime API and is excluded from the third-party ranking. One lead remains unresolved. See `cell.json`, `registry-snapshot.json`, `parsers.json`, `standard.json`, and `verification.json` for limits and evidence.

tspdf had zero primary GitHub stars at observation time; listing it records a verified reader, not proven adoption.

Both Magick paths use Ghostscript for PDF interpretation in the recorded build and do not add independent PDF syntax engines.

libvips loads PDF through its Poppler module in this pinned installation and shares that underlying parser with the Poppler path.
