# CPP × SVG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

exact primary GitHub repository stars.

| Rank | Package | Release | GitHub stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [imagemagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | parsed SVG dimensions and rendered red/green rectangle pixels | ImageMagick internal MSVG renderer with libxml2 |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | parsed SVG dimensions and rendered red/green rectangle pixels | libvips SVG loader over librsvg |
| 3 | [juce](https://docs.juce.com/develop/classjuce_1_1Drawable.html) | 9.0.5 | 9,142 | parsed SVG drawable bounds from local file | JUCE juce_graphics over bundled LunaSVG |
| 4 | [wxwidgets](https://github.com/wxWidgets/wxWidgets/blob/v3.3.4/include/wx/bmpbndl.h) | 3.3.4 | 7,301 | SVG dimensions and two rendered RGB pixels | wxWidgets wxBitmapBundle over bundled NanoSVG |
| 5 | [resvg](https://github.com/linebender/resvg/blob/v0.50.0/crates/c-api/resvg.h) | 0.50.0 | 4,185 | parsed SVG dimensions and rendered red/green rectangle pixels | resvg/usvg Rust SVG parser and tiny-skia renderer through C API |
| 6 | [thorvg](https://github.com/thorvg/thorvg/blob/v1.1.3/README.md) | 1.1.3 | 1,919 | parsed SVG document dimensions | ThorVG SVG loader and native vector engine |
| 7 | [lunasvg](https://github.com/sammycage/lunasvg/blob/v3.5.0/include/lunasvg.h) | 3.5.0 | 1,229 | parsed SVG dimensions and rendered red/green rectangle pixels | LunaSVG C++ document parser with PlutoVG rasterizer |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | [Debian installations (popcon)](https://sources.debian.org/src/gdk-pixbuf/) | 198,025 | parsed SVG dimensions and rendered red/green RGBA pixels | GdkPixbuf loader API with librsvg SVG plugin |
| 2 | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | [Debian installations (popcon)](https://sources.debian.org/src/librsvg/) | 192,430 | parsed SVG dimensions and rendered red/green rectangle pixels | librsvg Rust SVG engine through C API |
| 3 | [qtsvg](https://doc.qt.io/qt-6/qsvgrenderer.html) | 6.12.0 | [Debian installations (popcon)](https://sources.debian.org/src/qtsvg-opensource-src/) | 99,129 | parsed SVG dimensions and rendered red/green rectangle pixels | QtSvg QSvgRenderer document parser and Qt painter |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
