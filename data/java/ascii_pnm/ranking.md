# JAVA × ASCII PNM: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jai-imageio-core](https://github.com/jai-imageio/jai-imageio-core#jai-imageio-core-standalone) | 1.4.0 | 64 | ASCII PPM dimensions and red/green pixels | JAI ImageIO PNM plugin |
| 2 | [im4java](https://im4java.sourceforge.net/docs/dev-guide.html) | 1.4.0 | 37 | ASCII P3 PPM format and dimensions | im4java wrapper over host ImageMagick Netpbm decoder |
| 3 | [thumbnailator](https://github.com/coobird/thumbnailator/wiki/Examples) | 0.4.21 | 37 | ASCII PPM dimensions and red/green pixels | Thumbnailator wrapper over ImageIO PNM provider (TwelveMonkeys or JAI) |
| 4 | [openpnp-opencv](https://docs.opencv.org/4.9.0/d4/da8/group__imgcodecs.html) | 4.9.0-0 | 35 | ASCII PPM dimensions and red/green pixels | OpenPnP Java binding over native OpenCV PNM decoder |
| 5 | [commons-imaging](https://commons.apache.org/proper/commons-imaging/formatsupport.html) | 1.0.0-alpha6 | 27 | ASCII PPM dimensions and red/green pixels | Apache Commons Imaging PNM decoder |
| 6 | [ij](https://imagej.net/ij/developer/api/ij/ij/plugin/PGM_Reader.html) | 1.54p | 25 | ASCII PPM dimensions and red/green pixels | ImageJ PGM/PPM reader |
| 7 | [boofcv-io](https://boofcv.org/javadoc/boofcv/io/image/UtilImageIO.html) | 1.6.0 | 11 | ASCII PPM dimensions and red/green pixels | BoofCV ImageIO wrapper over PNM provider (TwelveMonkeys or JAI) |
| 8 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | 8.1.2-1.5.14 | 9 | ASCII P3 PPM codec and dimensions parsed from stream | Bytedeco binding to native FFmpeg PPM decoder |
| 9 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | 1.5.14 | 4 | ASCII P3 PPM decoded frame, codec and dimensions; pixel values not inspected | JavaCV wrapper over native FFmpeg PPM decoder |
| 10 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | 2024.08.29 | 2 | ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream | Jaffree wrapper over local FFprobe/FFmpeg |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
