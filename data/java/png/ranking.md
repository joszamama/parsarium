# Java × PNG: verified parser ranking

20 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T04:15:17.389021+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [pdfbox](https://javadoc.io/static/org.apache.pdfbox/pdfbox/3.0.8/org/apache/pdfbox/pdmodel/graphics/image/PDImageXObject.html) | org.apache.pdfbox:pdfbox:3.0.8 | 119 | PNG dimensions | Apache PDFBox image embedding path |
| 2 | [itextpdf](https://javadoc.io/static/com.itextpdf/itextpdf/5.5.13/com/itextpdf/text/pdf/codec/PngImage.html) | com.itextpdf:itextpdf:5.5.13 | 80 | PNG dimensions | iText 5 PNG codec |
| 3 | [jcodec](https://javadoc.io/static/org.jcodec/jcodec/0.2.5/org/jcodec/codecs/png/PNGDecoder.html) | org.jcodec:jcodec:0.2.5 | 44 | PNG dimensions | JCodec core PNG decoder |
| 4 | [jcodec-javase](https://javadoc.io/static/org.jcodec/jcodec-javase/0.2.5/org/jcodec/codecs/pngawt/PNGDecoder.html) | org.jcodec:jcodec-javase:0.2.5 | 41 | PNG dimensions | JCodec Java SE PNG wrapper over Java ImageIO |
| 5 | [thumbnailator](https://github.com/coobird/thumbnailator/wiki/Examples) | net.coobird:thumbnailator:0.4.21 | 37 | RGBA pixels | Thumbnailator image reader over Java ImageIO |
| 6 | [openpnp-opencv](https://github.com/openpnp/opencv) | org.openpnp:opencv:4.9.0-0 | 35 | PNG dimensions | OpenPnP Java JNI packaging of native OpenCV image decoder |
| 7 | [pngj](https://javadoc.io/static/ar.com.hjg/pngj/2.1.0/ar/com/hjg/pngj/PngReader.html) | ar.com.hjg:pngj:2.1.0 | 30 | RGBA pixels | PNGJ PNG decoder |
| 8 | [openpdf](https://javadoc.io/static/com.github.librepdf/openpdf/3.0.5/com.github.librepdf.openpdf/org/openpdf/text/ImageLoader.html) | com.github.librepdf:openpdf:3.0.5 | 29 | PNG dimensions | OpenPDF fork of iText; current PNG path over Java ImageIO |
| 9 | [commons-imaging](https://javadoc.io/static/org.apache.commons/commons-imaging/1.0.0-alpha6/org/apache/commons/imaging/Imaging.html) | org.apache.commons:commons-imaging:1.0.0-alpha6 | 27 | RGBA pixels | Apache Commons Imaging PNG decoder |
| 10 | [ij](https://imagej.net/ij/developer/api/ij/ij/io/Opener.html) | net.imagej:ij:1.54p | 25 | RGBA pixels | ImageJ image opener |
| 10 | [xmlgraphics-commons](https://xmlgraphics.apache.org/commons/image-loader.html) | org.apache.xmlgraphics:xmlgraphics-commons:2.12 | 25 | PNG dimensions and MIME | XML Graphics image loader over Java ImageIO |
| 12 | [lwjgl-stb](https://javadoc.lwjgl.org/org/lwjgl/stb/STBImage.html) | org.lwjgl:lwjgl-stb:3.4.3 | 22 | RGBA pixels | LWJGL binding to native stb_image PNG decoder |
| 13 | [boofcv-io](https://boofcv.org/javadoc/boofcv/io/image/UtilImageIO.html) | org.boofcv:boofcv-io:1.6.0 | 11 | RGBA pixels | BoofCV image I/O over Java ImageIO |
| 14 | [javafx-graphics](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/image/Image.html) | org.openjfx:javafx-graphics:21.0.9 | 9 | RGBA pixels | OpenJFX PNG image loader |
| 15 | [batik-codec](https://xmlgraphics.apache.org/batik/javadoc/org/apache/batik/ext/awt/image/codec/png/PNGImageDecoder.html) | org.apache.xmlgraphics:batik-codec:1.20 | 7 | RGBA pixels | Apache Batik PNG codec |
| 15 | [itext-io](https://api.itextpdf.com/iText/java/9.8.0/com/itextpdf/io/image/ImageDataFactory.html) | com.itextpdf:io:9.8.0 | 7 | PNG dimensions | iText 9 image I/O PNG codec |
| 17 | [jOpenDocument](https://javadoc.io/static/org.jopendocument/jOpenDocument/1.3/org/jopendocument/util/ImageInfo.html) | org.jopendocument:jOpenDocument:1.3 | 6 | PNG dimensions and format identity | jOpenDocument bundled ImageInfo header parser |
| 17 | [metadata-extractor](https://github.com/drewnoakes/metadata-extractor) | com.drewnoakes:metadata-extractor:2.22.0 | 6 | PNG dimensions | metadata-extractor PNG chunk reader |
| 19 | [pngtastic](https://github.com/depsypher/pngtastic/blob/master/src/main/java/com/googlecode/pngtastic/core/PngImage.java) | com.github.depsypher:pngtastic:1.8 | 1 | PNG dimensions | PNGTastic PNG chunk parser |
| 19 | [tika-image](https://tika.apache.org/4.2.0/api/org/apache/tika/parser/image/ImageParser.html) | org.apache.tika:tika-parser-image-module:4.2.0 | 1 | PNG dimensions | Apache Tika ImageParser over Java ImageIO |
