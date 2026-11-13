# C++ × SVG: verified parser ranking

17 verified third-party package paths; working goal 20, ceiling 30. Exact primary GitHub stars are compared only within this ecosystem. Stars measure broad project interest, not SVG-specific adoption. Homebrew name hits are discovery leads.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | SVG dimensions and two rendered pixels | internal MSVG renderer |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | SVG dimensions and two rendered pixels | libvips loader over librsvg |
| 3 | [JUCE](https://docs.juce.com/develop/classjuce_1_1Drawable.html) | 9.0.5 | 9,142 | parsed SVG drawable bounds from local file | JUCE over bundled LunaSVG |
| 4 | [resvg](https://github.com/linebender/resvg/blob/v0.50.0/crates/c-api/resvg.h) | 0.50.0 | 4,185 | SVG dimensions and two rendered pixels | resvg/usvg Rust SVG engine |
| 5 | [ThorVG](https://github.com/thorvg/thorvg/blob/v1.1.3/README.md) | 1.1.3 | 1,919 | SVG root dimensions | ThorVG SVG loader |
| 6 | [LunaSVG](https://github.com/sammycage/lunasvg/blob/v3.5.0/include/lunasvg.h) | 3.5.0 | 1,229 | SVG dimensions and two rendered pixels | LunaSVG parser with PlutoVG rasterizer |
| 7 | [SDL3_image](https://wiki.libsdl.org/SDL3_image/IMG_LoadSVG_IO) | 3.4.8 | 997 | SVG dimensions and two rendered RGBA pixels | embedded NanoSVG parser |
| 8 | [PlutoSVG](https://github.com/sammycage/plutosvg/blob/v0.0.8/source/plutosvg.h) | 0.0.8 | 464 | SVG dimensions and two rendered pixels | PlutoSVG parser with PlutoVG rasterizer |
| 9 | [NovaSVG](https://mohammadraziei.github.io/novasvg/index.html) | 0.11.5 | 13 | SVG root dimensions and two parsed rectangle elements | NovaSVG native C++ SVG parser |
| unranked | [GdkPixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | unknown | SVG dimensions and two rendered RGBA pixels | librsvg SVG plugin |
| unranked | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | unknown | SVG dimensions and two rendered pixels | librsvg Rust SVG engine |
| unranked | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | unknown | SVG dimensions and two rendered pixels | SVG-to-MVG coder with libxml2 |
| unranked | [QtSvg](https://doc.qt.io/qt-6/qsvgrenderer.html) | 6.12.0 | unknown | SVG dimensions and two rendered pixels | QtSvg QSvgRenderer and Qt painter |
| unranked | [QtBase QImageReader](https://doc.qt.io/qt-6/qimagereader.html) | 6.12.0 | unknown | SVG dimensions and two rendered pixels | QtSvg image plugin |
| unranked | [libsvgtiny](https://www.netsurf-browser.org/projects/libsvgtiny/) | 0.1.8 | unknown | SVG dimensions, two shapes and fill colors | libsvgtiny over libdom |
| unranked | [libsvg](https://cairographics.org/snapshots/libsvg-0.1.4.tar.gz) | 0.1.4 | unknown | SVG root dimensions | libsvg over libxml2 |
| unranked | [libsvg-cairo](https://cairographics.org/snapshots/libsvg-cairo-0.1.6.tar.gz) | 0.1.6 | unknown | SVG dimensions and two rendered pixels | libsvg parser with Cairo |

libvips and GdkPixbuf share librsvg; libsvg-cairo shares libsvg. PlutoSVG and LunaSVG share PlutoVG rasterization but retain separate SVG document parsers. JUCE bundles LunaSVG and exposes its own C++ Drawable API. QtSvg is a separate Qt module with its own document reader; QtBase QImageReader uses that QtSvg image plugin. No recorded leads remain unresolved; 3 additional verified paths are needed. See `cell.json`, `registry-snapshot.json`, and `verification.json`.
