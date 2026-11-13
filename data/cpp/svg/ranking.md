# C++ × SVG: verified parser ranking

7 verified third-party package paths; working goal 20, ceiling 30. Exact primary GitHub stars are compared only within this ecosystem. Stars measure broad project interest, not SVG-specific adoption. Homebrew name hits are discovery leads.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | SVG dimensions and two rendered pixels | internal MSVG renderer |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | SVG dimensions and two rendered pixels | libvips loader over librsvg |
| 3 | [resvg](https://github.com/linebender/resvg/blob/v0.50.0/crates/c-api/resvg.h) | 0.50.0 | 4,185 | SVG dimensions and two rendered pixels | resvg/usvg Rust SVG engine |
| 4 | [LunaSVG](https://github.com/sammycage/lunasvg/blob/v3.5.0/include/lunasvg.h) | 3.5.0 | 1,229 | SVG dimensions and two rendered pixels | LunaSVG parser with PlutoVG rasterizer |
| 5 | [PlutoSVG](https://github.com/sammycage/plutosvg/blob/v0.0.8/source/plutosvg.h) | 0.0.8 | 464 | SVG dimensions and two rendered pixels | PlutoSVG parser with PlutoVG rasterizer |
| unranked | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | unknown | SVG dimensions and two rendered pixels | librsvg Rust SVG engine |
| unranked | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | unknown | SVG dimensions and two rendered pixels | SVG-to-MVG coder with libxml2 |

libvips shares librsvg. PlutoSVG and LunaSVG share PlutoVG rasterization but retain separate SVG document parsers. 3 leads remain unresolved, and 13 additional verified paths are needed. See `cell.json`, `registry-snapshot.json`, and `verification.json`.
