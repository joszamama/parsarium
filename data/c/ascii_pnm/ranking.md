# C × ASCII_PNM: verified parser ranking

20 verified third-party package paths; working goal 20, ceiling 30. The metric is primary GitHub repository stars captured at 2026-11-12T15:32:36.147780+00:00. Conan recipe-name matches provide no comparable per-recipe downloads. Stars are a broad-project adoption proxy, compared only within C, and do not establish a complete most-used set. 10 paths have no comparable primary GitHub metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,117 | P3 codec identification, dimensions, and two decoded RGB pixels | FFmpeg native PNM decoder |
| 2 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-35 | 17,850 | P3 dimensions and two decoded RGBA pixels | ImageMagick PNM coder |
| 3 | [vips](https://www.libvips.org/API/current/VipsImage.html) | 8.18.7 | 11,801 | P3 dimensions and two decoded RGB pixels | libvips PPM loader |
| 4 | [leptonica](https://github.com/DanBloomberg/leptonica/blob/1.87.0/src/allheaders.h) | 1.87.0 | 2,107 | P3 dimensions and two decoded RGB pixels | Leptonica PNM reader |
| 5 | [sdl2_image](https://wiki.libsdl.org/SDL2_image/IMG_Load) | 2.8.12 | 997 | P3 dimensions and two decoded RGBA pixels | SDL_image PNM decoder lineage |
| 5 | [sdl3_image](https://wiki.libsdl.org/SDL3_image/IMG_Load) | 3.4.8 | 997 | P3 dimensions and two decoded RGBA pixels | SDL_image PNM decoder lineage |
| 7 | [sail](https://github.com/HappySeaFox/sail/blob/v1.3.1/src/sail/sail_junior.h) | 1.3.1 | 362 | P3 dimensions and two decoded RGB pixels | SAIL native PNM codec |
| 8 | [jasper](https://jasper-software.github.io/jasper-manual/latest/html/group__module__images.html) | 4.2.9 | 262 | P3 dimensions and two decoded RGB pixels | JasPer PNM codec |
| 9 | [libimago](https://github.com/jtsiomb/libimago/blob/v2.4.2/README.md) | 2.4.2 | 48 | P3 dimensions and two decoded RGB pixels | libimago PPM reader |
| 10 | [libpnmio](https://github.com/nkkav/libpnmio/blob/bd860723211ffdb3a0b0a7067afd7e94d583af7c/README.rst) | 1.2.7 (README; commit pinned) | 21 | P3 dimensions and two decoded RGB pixels, maxval | libpnmio PPM reader |
| unranked | [devil](https://openil.sourceforge.net/docs/DevIL%20Reference%20Guide.pdf) | 1.8.0 | unknown | P3 dimensions and two decoded RGBA pixels | DevIL PNM reader |
| unranked | [freeimage](https://freeimage.sourceforge.io/fnet/html/99F7C60B.htm) | 3.18.0 | unknown | P3 dimensions and two decoded RGB pixels | FreeImage PPM plugin |
| unranked | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | unknown | P3 dimensions and two decoded RGB pixels | GdkPixbuf PNM loader |
| unranked | [gegl](https://www.gegl.org/operations/gegl-ppm-load.html) | 0.4.72 | unknown | P3 dimensions and two decoded RGB pixels | GEGL PPM loader |
| unranked | [graphicsmagick](https://graphicsmagick.sourceforge.io/wand/magick_wand.html) | 1.3.49 | unknown | P3 dimensions and two decoded RGBA pixels | GraphicsMagick PNM coder |
| unranked | [gstreamer](https://gstreamer.freedesktop.org/documentation/pnm/pnmdec.html) | 1.28.9 | unknown | P3 dimensions, RGB caps, and two decoded pixels | GStreamer gst-plugins-bad pnmdec |
| unranked | [imlib2](https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/) | 1.12.7 | unknown | P3 dimensions and two decoded RGBA pixels | Imlib2 PNM loader |
| unranked | [imtoolkit](https://www.tecgraf.puc-rio.br/im/en/storage_guide.html) | 3.15 | unknown | P3 dimensions and two decoded RGB pixels | IM Toolkit PNM driver |
| unranked | [libpnmrw](https://acme.com/software/libpnmrw/) | 14Aug2014 | unknown | P3 dimensions, maxval, and two decoded RGB pixels | libpnmrw PBMPLUS-derived parser |
| unranked | [netpbm](https://netpbm.sourceforge.net/doc/libppm.html) | 11.02.30 | unknown | P3 dimensions, maxval, and two decoded RGB pixels | Netpbm libppm parser |
