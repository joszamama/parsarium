# CPP × ASCII PNM: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub stars of primary upstream repository, where available.

| Rank | Package | Release | GitHub stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,107 | P3 codec identification, dimensions, and two decoded RGB pixels | FFmpeg native PNM decoder |
| 2 | [imagemagick](https://imagemagick.org/magick-wand/) | 7.1.2-35 | 17,848 | P3 dimensions and two decoded RGBA pixels | ImageMagick PNM coder |
| 3 | [vips](https://www.libvips.org/API/current/VipsImage.html) | 8.18.7 | 11,801 | P3 dimensions and two decoded RGB pixels | libvips PPM loader |
| 4 | [wxwidgets](https://wxwidgets.org/docs/book/Cross-Platform%20GUI%20Programming%20with%20wxWidgets.pdf) | 3.3.4 | 7,299 | P3 dimensions and two decoded RGBA pixels | wxWidgets native PNM handler |
| 5 | [qtbase](https://doc.qt.io/qt-6/qimagereader.html) | 6.12.0 | 3,122 | P3 dimensions and two decoded RGBA pixels | QtBase native QPPMHandler |
| 6 | [openimageio](https://openimageio.readthedocs.io/en/v3.2.2.0/imageinput.html) | 3.2.2.0 | 2,403 | P3 format identification, ASCII encoding flag, dimensions, and two decoded RGB pixels | OpenImageIO native PNM plugin |
| 7 | [leptonica](https://github.com/DanBloomberg/leptonica/blob/1.87.0/src/allheaders.h) | 1.87.0 | 2,107 | P3 dimensions and two decoded RGB pixels | Leptonica PNM reader |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [gdk-pixbuf](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) | 2.44.8 | [Debian installations (popcon)](https://sources.debian.org/src/gdk-pixbuf/) | 198,025 | P3 dimensions and two decoded RGB pixels | GdkPixbuf PNM loader |
| 2 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pnm/pnmdec.html) | 1.28.9 | [Debian installations (popcon)](https://sources.debian.org/src/gstreamer1.0/) | 172,612 | P3 dimensions, RGB caps, and two decoded pixels | GStreamer gst-plugins-bad pnmdec |
| 3 | [netpbm](https://netpbm.sourceforge.net/doc/libppm.html) | 11.02.30 | [Debian installations (popcon)](https://sources.debian.org/src/netpbm-free/) | 82,331 | P3 dimensions, maxval, and two decoded RGB pixels | Netpbm libppm parser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
