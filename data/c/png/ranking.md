# C × PNG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub repository stargazers_count. Repository stars are an adoption proxy, not package downloads. Values are compared only within C. Six primary upstreams outside GitHub remain unranked; mirror stars would be a different signal. SDL2_image and SDL3_image share a project and its star count. Recipe-name hits are discovery, not this ranking.

| Rank | Package | Release | GitHub stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,637 | pixels | raylib bundled stb_image PNG decoder |
| 2 | [stb](https://github.com/nothings/stb/blob/a7d4c2175630e1ea5b6f8dd00ab96fed0b97b96d/stb_image.h) | cci.20261021 | 35,006 | pixels | stb_image |
| 3 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-35 | 17,848 | pixels | ImageMagick PNG coder (libpng-backed) |
| 4 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadPNG) | 3.4.20 | 16,974 | pixels | SDL3 bundled stb_image PNG decoder |
| 5 | [vips](https://www.libvips.org/API/current/VipsImage.html) | 8.18.7 | 11,801 | pixels | libvips PNG loader (libpng-backed) |
| 6 | [wuffs](https://github.com/google/wuffs/blob/v0.3.6/doc/std/image-decoders.md) | 0.3.6 | 4,881 | PNG image configuration | Wuffs PNG decoder |
| 7 | [lodepng](https://github.com/lvandeve/lodepng/blob/865adac2b8149774401626101ec618e3de45e1d8/lodepng.h) | cci.20260102 | 2,357 | pixels | LodePNG |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [cairo](https://www.cairographics.org/manual/cairo-PNG-Support.html) | 1.18.6 | [Debian installations (popcon)](https://sources.debian.org/src/cairo/) | 208,328 | pixels | Cairo PNG surface loader (libpng-backed) |
| 2 | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | [Debian installations (popcon)](https://sources.debian.org/src/gdk-pixbuf/) | 198,025 | pixels | GdkPixbuf PNG loader (libpng-backed) |
| 3 | [imlib2](https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/) | 1.12.7 | [Debian installations (popcon)](https://sources.debian.org/src/imlib2/) | 20,958 | pixels | Imlib2 PNG loader (libpng-backed) |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
