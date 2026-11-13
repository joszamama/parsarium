# C × PDF: verified parser ranking

16 verified third-party package paths; working goal 20, ceiling 30. The primary adoption metric is Homebrew install-on-request events for 2025-11-13 through 2026-11-13, compared only within this cell. It measures whole formulae, not PDF-specific use or independent parser engines. Six verified paths have no comparable formula metric and remain unranked. The previous primary GitHub-star snapshot is preserved separately as an auxiliary project-interest signal in `registry-snapshot.json`.

| Rank | Package | Pinned release | Requested installs (365d) | Verified scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 778,693 | rendered PDF page and dimensions | ImageMagick PDF coder + Ghostscript |
| 2 | [Poppler GLib](https://poppler.freedesktop.org/api/glib/PopplerDocument.html) | 26.11.0 | 688,177 | parsed PDF page count | Poppler PDF parser |
| 3 | [Ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | 181,380 | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| 4 | [qpdf C API](https://github.com/qpdf/qpdf/blob/v12.4.2/include/qpdf/qpdf-c.h) | 12.4.2 | 65,652 | parsed PDF page count | qpdf C API over C++ parser |
| 5 | [libvips](https://www.libvips.org/API/current/ctor.Image.pdfload.html) | 8.18.7 | 60,878 | PDF page count and first page dimensions | vips-poppler module over Poppler |
| 6 | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | 38,391 | rendered PDF page and dimensions | GraphicsMagick PDF coder + Ghostscript |
| 7 | [MuPDF](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | 11,659 | parsed PDF page count | MuPDF C parser |
| 8 | [Evince libdocument](https://gnome.pages.gitlab.gnome.org/evince/document/class.Document.html) | 48.4 | 1,757 | two-page PDF page count | Evince PDF backend over Poppler GLib |
| 9 | [GNOME Papers libdocument](https://gnome.pages.gitlab.gnome.org/papers/document/class.Document.html) | 51.1 | 712 | two-page PDF page count | GNOME Papers PDF backend over Poppler GLib |
| 10 | [PDFio](https://www.msweet.org/pdfio/pdfio.html) | 1.6.5 | 6 | parsed PDF page count and first page object | PDFio parser |
| unranked | [PDFium](https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md) | 159.0.8152.0 | unknown | parsed PDF page count and first page object | PDFium parser |
| unranked | [Vanilla.PDF](https://vanillapdf.readthedocs.io/en/stable/c_api.html) | 2.3.0 | unknown | parsed PDF page count and first page object | Vanilla.PDF C API over C++ parser |
| unranked | [tspdf](https://github.com/be-lang/tspdf/blob/v0.5.1/docs/library.md) | 0.5.1 | unknown | parsed PDF page count and first page | tspdf C11 parser |
| unranked | [pdf_oxide](https://github.com/yfedoseev/pdf_oxide/blob/v0.3.78/include/pdf_oxide_c/pdf_oxide.h) | 0.3.78 | unknown | parsed PDF page count | Rust pdf_oxide engine via C ABI |
| unranked | [LibreOfficeKit](https://github.com/LibreOffice/core/blob/libreoffice-26.8.3.1/include/LibreOfficeKit/LibreOfficeKit.h) | 26.8.3.1 | unknown | two-page PDF imported as Draw document | LibreOffice PDF import through C ABI |
| unranked | [unpdf C ABI](https://github.com/iyulab/unpdf/blob/v0.54.0/src/ffi.rs) | 0.54.0 | unknown | parsed PDF page-tree count | unpdf Rust PDF parser via C ABI |

The formula metric is from the [Homebrew 365-day requested-install snapshot](https://formulae.brew.sh/api/analytics/install-on-request/365d.json). `poppler-glib` maps to the `poppler` formula, and `libvips` maps to `vips`. PDFio was verified from tagged source, while its formula-wide requested-install count is used only as an adoption proxy. The ordering does not establish a definitive most-used top 20 because six paths lack this metric, the search is bounded, and four more verified paths are needed.

ImageMagick and GraphicsMagick use Ghostscript for PDF interpretation in this installation. libvips, Evince, and GNOME Papers use Poppler; their installed PDF backends directly link the same pinned Poppler GLib library as the separately verified C API. LibreOfficeKit's bundled `xpdfimport` has Poppler markers, but its exact import call path was not traced. These are distinct package input APIs, not independent syntax engines. Apple Core Graphics is a verified macOS runtime API and is outside this third-party ranking.

LibreOffice's 416,680 Homebrew **cask** install events in the same year are an auxiliary whole-application signal; cask events are not mixed with formula requested installs. The tagged LibreOfficeKit, Evince, and GNOME Papers C APIs passed the valid two-page local PDF control. One other C wrapper lead remains unresolved. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json` for limits and control evidence.

The unpdf 0.54.0 C ABI was built from its pinned crates.io source and bundled Cargo.lock, then parsed the one-page PDF through its local-file API. It shares the verified Rust unpdf parser family. The upstream project's 65 observed GitHub stars are recorded only as auxiliary interest; they do not establish C API adoption.

GNOME Papers 51.1 parsed the valid two-page local PDF through its documented C document library. Its public umbrella header asks callers to define a macro asserting contact with authors because the API is unstable; the adapter mirrors signatures from hash-pinned upstream headers and does not assert such contact. The Homebrew requested-install count measures the whole GNOME Papers formula, not use of its C API.
