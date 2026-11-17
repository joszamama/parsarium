# C × PDF: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-35 | 778,693 | Rendered PDF page sequence and first page dimensions | ImageMagick PDF coder + Ghostscript PDF interpreter |
| 2 | [poppler-glib](https://poppler.freedesktop.org/api/glib/PopplerDocument.html) | 26.11.0 | 688,177 | PDF document page count | Poppler PDF parser, GLib C frontend |
| 3 | [ghostscript](https://ghostscript.readthedocs.io/en/master/Language.html) | 10.08.0 | 181,380 | PDF interpreter NumPages metadata | Ghostscript PDF interpreter |
| 4 | [qpdf](https://github.com/qpdf/qpdf/blob/v12.4.2/include/qpdf/qpdf-c.h) | 12.4.2 | 65,652 | PDF document page count | qpdf C API over C++ PDF parser |
| 5 | [libvips](https://www.libvips.org/API/current/ctor.Image.pdfload.html) | 8.18.7 | 60,878 | PDF page count and first page dimensions from PDF loader header | libvips vips-poppler module over Poppler PDF parser |
| 6 | [graphicsmagick](https://graphicsmagick.sourceforge.io/wand/magick_wand.html) | 1.3.49 | 38,391 | Rendered PDF page sequence and first page dimensions | GraphicsMagick PDF coder + Ghostscript PDF interpreter |
| 7 | [mupdf](https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html) | 1.28.6 | 11,659 | PDF document page count | MuPDF C document parser |
| 8 | [evince](https://gnome.pages.gitlab.gnome.org/evince/document/class.Document.html) | 48.4 | 1,757 | PDF page count through Evince libdocument C API | Evince PDF backend over Poppler GLib |
| 9 | [gnome-papers](https://gnome.pages.gitlab.gnome.org/papers/document/class.Document.html) | 51.1 | 712 | PDF document page count | GNOME Papers PDF backend over Poppler GLib |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [atril](https://github.com/mate-desktop/atril/blob/v1.28.2/libdocument/ev-document-factory.h) | 1.28.2 | [Debian source installed count](https://sources.debian.org/src/atril/) | 35,152 | PDF page count through Atril libdocument C API | Atril PDF backend over Poppler GLib |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
