# C × PNG: verified parser ranking

20 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured at 2026-11-12T07:20:18.790315+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 6 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,637 | pixels | raylib bundled stb_image PNG decoder |
| 2 | [stb](https://github.com/nothings/stb/blob/a7d4c2175630e1ea5b6f8dd00ab96fed0b97b96d/stb_image.h) | cci.20261021 | 35,006 | pixels | stb_image |
| 3 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-35 | 17,848 | pixels | ImageMagick PNG coder (libpng-backed) |
| 4 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadPNG) | 3.4.20 | 16,974 | pixels | SDL3 bundled stb_image PNG decoder |
| 5 | [vips](https://www.libvips.org/API/current/VipsImage.html) | 8.18.7 | 11,801 | pixels | libvips PNG loader (libpng-backed) |
| 6 | [wuffs](https://github.com/google/wuffs/blob/v0.3.6/doc/std/image-decoders.md) | 0.3.6 | 4,881 | PNG image configuration | Wuffs PNG decoder |
| 7 | [lodepng](https://github.com/lvandeve/lodepng/blob/865adac2b8149774401626101ec618e3de45e1d8/lodepng.h) | cci.20260102 | 2,357 | pixels | LodePNG |
| 8 | [leptonica](https://github.com/DanBloomberg/leptonica/blob/1.87.0/src/allheaders.h) | 1.87.0 | 2,107 | RGB pixels | Leptonica PNG loader (libpng-backed) |
| 9 | [libpng](https://github.com/pnggroup/libpng/blob/v1.6.59/example.c) | 1.6.59 | 1,679 | pixels | libpng |
| 10 | [sdl2_image](https://wiki.libsdl.org/SDL2_image/IMG_Load) | 2.8.12 | 997 | pixels | SDL_image 2 PNG loader (libpng-backed) |
| 10 | [sdl3_image](https://wiki.libsdl.org/SDL3_image/IMG_Load) | 3.4.8 | 997 | pixels | SDL_image 3 PNG loader (libpng in recorded build) |
| 12 | [gd](https://github.com/libgd/libgd/blob/gd-2.3.3/src/gd.h) | 2.3.3 | 989 | pixels | GD PNG codec (libpng-backed) |
| 13 | [libspng](https://github.com/randy408/libspng/blob/v0.7.4/spng/spng.h) | 0.7.4 | 851 | pixels | libspng |
| 14 | [pngle](https://github.com/kikuchan/pngle/blob/v1.1.0/src/pngle.h) | 1.1.0 | 141 | pixels | pngle with bundled miniz |
| unranked | [cairo](https://www.cairographics.org/manual/cairo-PNG-Support.html) | 1.18.6 | unknown | pixels | Cairo PNG surface loader (libpng-backed) |
| unranked | [devil](https://openil.sourceforge.net/docs/DevIL%20Reference%20Guide.pdf) | 1.8.0 | unknown | pixels | DevIL PNG loader (libpng-backed) |
| unranked | [freeimage](https://freeimage.sourceforge.io/faq.html) | 3.18.0 | unknown | pixels | FreeImage PNG plugin (bundled libpng lineage) |
| unranked | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | unknown | pixels | GdkPixbuf PNG loader (libpng-backed) |
| unranked | [graphicsmagick](https://graphicsmagick.sourceforge.io/wand/magick_wand.html) | 1.3.49 | unknown | pixels | GraphicsMagick PNG coder (libpng-backed) |
| unranked | [imlib2](https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/) | 1.12.7 | unknown | pixels | Imlib2 PNG loader (libpng-backed) |
