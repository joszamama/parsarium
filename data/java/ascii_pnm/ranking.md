# Java × ASCII PNM: verified parser ranking

16 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T20:28:43.776768+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

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
| 9 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | com.github.kokorin.jaffree:jaffree:2024.08.29 | 2 | ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream | Jaffree wrapper over local FFprobe/FFmpeg |
| 10 | [tika-image](https://tika.apache.org/docs/4.0.x/formats.html) | org.apache.tika:tika-parser-image-module:4.2.0 | 1 | ASCII PPM image width and height | Apache Tika ImageParser over ImageIO PNM provider (TwelveMonkeys or JAI) |
| 11 | [bramp-ffmpeg](https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar) | net.bramp.ffmpeg:ffmpeg:0.9.2 | 0 | ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream | bramp FFprobe CLI wrapper over FFmpeg |
| 11 | [imageio-native-magick](https://github.com/ghosthack/imageio-native#imagemagick) | io.github.ghosthack:imageio-native-magick:2.0.0 | 0 | ASCII PPM dimensions and red/green pixels | imageio-native-magick wrapper over ImageMagick Netpbm decoder |
| 11 | [imageio-native-vips](https://github.com/ghosthack/imageio-native#optional-backends) | io.github.ghosthack:imageio-native-vips:2.0.0 | 0 | ASCII PPM dimensions and red/green pixels | imageio-native-vips wrapper over libvips Netpbm decoder |
| 11 | [imageio-pnm](https://github.com/haraldk/TwelveMonkeys#file-formats-supported) | com.twelvemonkeys.imageio:imageio-pnm:3.15.3 | 0 | ASCII PPM dimensions and red/green pixels | TwelveMonkeys PNM ImageIO plugin |
| 11 | [imagic-ffmpeg-java](https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar) | ch.imagic:ffmpeg-java:0.1.2 | 0 | ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream | Imagic fork of bramp FFprobe CLI wrapper over FFmpeg |
| 11 | [v47-jaffree](https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar) | io.v47.jaffree:jaffree:2.1.0 | 0 | ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream | v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg |
