# C × PNG: verified parser ranking

14 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured at 2026-11-12T07:12:51.056143+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 3 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [stb](https://github.com/nothings/stb/blob/a7d4c2175630e1ea5b6f8dd00ab96fed0b97b96d/stb_image.h) | cci.20261021 | 35,006 | pixels | stb_image |
| 2 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-31 | 17,848 | pixels | ImageMagick PNG coder (libpng-backed) |
| 3 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadPNG) | 3.4.20 | 16,974 | pixels | SDL3 bundled stb_image PNG decoder |
| 4 | [vips](https://www.libvips.org/API/current/VipsImage.html) | 8.18.7 | 11,801 | pixels | libvips PNG loader (libpng-backed) |
| 5 | [lodepng](https://github.com/lvandeve/lodepng/blob/865adac2b8149774401626101ec618e3de45e1d8/lodepng.h) | cci.20260102 | 2,357 | pixels | LodePNG |
| 6 | [libpng](https://github.com/pnggroup/libpng/blob/v1.6.59/example.c) | 1.6.59 | 1,679 | pixels | libpng |
| 7 | [sdl2_image](https://wiki.libsdl.org/SDL2_image/IMG_Load) | 2.8.12 | 997 | pixels | SDL_image 2 PNG loader (libpng-backed) |
| 7 | [sdl3_image](https://wiki.libsdl.org/SDL3_image/IMG_Load) | 3.4.8 | 997 | pixels | SDL_image 3 PNG loader (libpng in recorded build) |
| 9 | [gd](https://github.com/libgd/libgd/blob/gd-2.3.3/src/gd.h) | 2.3.3 | 989 | pixels | GD PNG codec (libpng-backed) |
| 10 | [libspng](https://github.com/randy408/libspng/blob/v0.7.4/spng/spng.h) | 0.7.4 | 851 | pixels | libspng |
| 11 | [pngle](https://github.com/kikuchan/pngle/blob/v1.1.0/src/pngle.h) | 1.1.0 | 141 | pixels | pngle with bundled miniz |
| unranked | [cairo](https://www.cairographics.org/manual/cairo-PNG-Support.html) | 1.18.6 | unknown | pixels | Cairo PNG surface loader (libpng-backed) |
| unranked | [freeimage](https://freeimage.sourceforge.io/faq.html) | 3.18.0 | unknown | pixels | FreeImage PNG plugin (bundled libpng lineage) |
| unranked | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | unknown | pixels | GdkPixbuf PNG loader (libpng-backed) |
