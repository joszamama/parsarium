# C++ × SVG: verified parser ranking

4 verified third-party package paths; working goal 20, ceiling 30. Only exact stars of primary GitHub repositories are compared within this ecosystem. GitHub stars measure broad project interest, not SVG-specific adoption. Homebrew name hits are discovery leads.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ImageMagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | SVG dimensions and two rendered pixels | internal MSVG renderer with libxml2 |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | SVG dimensions and two rendered pixels | libvips loader over librsvg |
| unranked | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | unknown | SVG dimensions and two rendered pixels | librsvg Rust SVG engine |
| unranked | [GraphicsMagick](https://graphicsmagick.sourceforge.io/formats.html) | 1.3.49 | unknown | SVG dimensions and two rendered pixels | SVG-to-MVG coder with libxml2 |

libvips shares librsvg; both Magick coders use system libxml2 but have separate SVG logic. Six leads are unresolved, and 16 additional verified paths are needed. See `cell.json`, `registry-snapshot.json`, and `verification.json`.
