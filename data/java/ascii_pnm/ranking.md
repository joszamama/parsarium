# Java × ASCII PNM: verified parser ranking

12 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T20:25:06.438070+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jai-imageio-core](https://github.com/jai-imageio/jai-imageio-core#jai-imageio-core-standalone) | com.github.jai-imageio:jai-imageio-core:1.4.0 | 64 | ASCII PPM dimensions and red/green pixels | JAI ImageIO PNM plugin |
| 2 | [thumbnailator](https://github.com/coobird/thumbnailator/wiki/Examples) | net.coobird:thumbnailator:0.4.21 | 37 | ASCII PPM dimensions and red/green pixels | Thumbnailator wrapper over ImageIO PNM provider (TwelveMonkeys or JAI) |
| 3 | [openpnp-opencv](https://docs.opencv.org/4.9.0/d4/da8/group__imgcodecs.html) | org.openpnp:opencv:4.9.0-0 | 35 | ASCII PPM dimensions and red/green pixels | OpenPnP Java binding over native OpenCV PNM decoder |
| 4 | [commons-imaging](https://commons.apache.org/proper/commons-imaging/formatsupport.html) | org.apache.commons:commons-imaging:1.0.0-alpha6 | 27 | ASCII PPM dimensions and red/green pixels | Apache Commons Imaging PNM decoder |
| 5 | [ij](https://imagej.net/ij/developer/api/ij/ij/plugin/PGM_Reader.html) | net.imagej:ij:1.54p | 25 | ASCII PPM dimensions and red/green pixels | ImageJ PGM/PPM reader |
| 6 | [boofcv-io](https://boofcv.org/javadoc/boofcv/io/image/UtilImageIO.html) | org.boofcv:boofcv-io:1.6.0 | 11 | ASCII PPM dimensions and red/green pixels | BoofCV ImageIO wrapper over PNM provider (TwelveMonkeys or JAI) |
| 7 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | org.bytedeco:ffmpeg:8.1.2-1.5.14 | 9 | ASCII P3 PPM codec and dimensions parsed from stream | Bytedeco binding to native FFmpeg PPM decoder |
| 8 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | org.bytedeco:javacv:1.5.14 | 4 | ASCII P3 PPM decoded frame, codec and dimensions; pixel values not inspected | JavaCV wrapper over native FFmpeg PPM decoder |
| 9 | [tika-image](https://tika.apache.org/docs/4.0.x/formats.html) | org.apache.tika:tika-parser-image-module:4.2.0 | 1 | ASCII PPM image width and height | Apache Tika ImageParser over ImageIO PNM provider (TwelveMonkeys or JAI) |
| 10 | [imageio-native-magick](https://github.com/ghosthack/imageio-native#imagemagick) | io.github.ghosthack:imageio-native-magick:2.0.0 | 0 | ASCII PPM dimensions and red/green pixels | imageio-native-magick wrapper over ImageMagick Netpbm decoder |
| 10 | [imageio-native-vips](https://github.com/ghosthack/imageio-native#optional-backends) | io.github.ghosthack:imageio-native-vips:2.0.0 | 0 | ASCII PPM dimensions and red/green pixels | imageio-native-vips wrapper over libvips Netpbm decoder |
| 10 | [imageio-pnm](https://github.com/haraldk/TwelveMonkeys#file-formats-supported) | com.twelvemonkeys.imageio:imageio-pnm:3.15.3 | 0 | ASCII PPM dimensions and red/green pixels | TwelveMonkeys PNM ImageIO plugin |
