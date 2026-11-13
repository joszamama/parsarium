# C++ × SVG: verified parser ranking

2 verified third-party package paths; working goal 20, ceiling 30. Only exact stars of primary GitHub repositories are compared within this ecosystem. GitHub stars measure project interest, not SVG-specific adoption; Homebrew formula-name hits are discovery leads.

| Rank | Package | Pinned release | Primary GitHub stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | SVG dimensions and two rendered pixels | libvips loader over librsvg |
| unranked | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | unknown | SVG dimensions and two rendered pixels | librsvg Rust SVG engine |

libvips links librsvg; these are distinct package APIs over one SVG syntax engine. Eight leads are unresolved, and 18 additional verified paths are needed for the working goal. See `cell.json`, `registry-snapshot.json`, and `verification.json`.
