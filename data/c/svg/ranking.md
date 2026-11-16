# C × SVG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

exact primary GitHub repository stars.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [imagemagick](https://imagemagick.org/formats/) | 7.1.2-35 | 17,852 | parsed SVG dimensions and rendered red/green rectangle pixels | ImageMagick internal MSVG renderer with libxml2 |
| 2 | [libvips](https://www.libvips.org/API/current/ctor.Image.svgload.html) | 8.18.7 | 11,801 | parsed SVG dimensions and rendered red/green rectangle pixels | libvips SVG loader over librsvg |
| 3 | [resvg](https://github.com/linebender/resvg/blob/v0.50.0/crates/c-api/resvg.h) | 0.50.0 | 4,185 | parsed SVG dimensions and rendered red/green rectangle pixels | resvg/usvg Rust SVG parser and tiny-skia renderer through C API |
| 4 | [nanosvg](https://github.com/memononen/nanosvg#parser) | 2023-12-29 | 2,039 | SVG root dimensions and two parsed rectangle shapes with paths | NanoSVG native SVG parser |
| 5 | [thorvg](https://github.com/thorvg/thorvg/blob/v1.1.3/README.md) | 1.1.3 | 1,919 | parsed SVG document dimensions | ThorVG SVG loader and native vector engine |
| 6 | [sdl2_image](https://wiki.libsdl.org/SDL2_image/IMG_LoadSVG_RW) | 2.8.12 | 997 | SVG dimensions and two rendered RGBA pixels through SDL2_image's format-specific reader | SDL2_image SVG loader embedding NanoSVG |
| 7 | [sdl3_image](https://wiki.libsdl.org/SDL3_image/IMG_LoadSVG_IO) | 3.4.8 | 997 | parsed SVG dimensions and rendered red/green RGBA pixels | SDL3_image SVG loader with embedded NanoSVG parser/rasterizer |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | [Debian source installed count](https://sources.debian.org/src/gdk-pixbuf/) | 198,025 | parsed SVG dimensions and rendered red/green RGBA pixels | GdkPixbuf loader API with librsvg SVG plugin |
| 2 | [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html) | 2.63.4 | [Debian source installed count](https://sources.debian.org/src/librsvg/) | 192,430 | parsed SVG dimensions and rendered red/green rectangle pixels | librsvg Rust SVG engine through C API |
| 3 | [gtk4](https://docs.gtk.org/gtk4/ctor.Svg.new_from_bytes.html) | 4.24.1 | [Debian source installed count](https://sources.debian.org/src/gtk4/) | 178,888 | SVG root dimensions parsed by GtkSvg from local file bytes | GTK 4 native GtkSvg parser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
