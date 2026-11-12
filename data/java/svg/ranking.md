# Java × SVG: verified parser ranking

15 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T19:47:26.145260+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 4 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jsvg](https://github.com/weisJ/jsvg) | com.github.weisj:jsvg:2.0.0 | 26 | Rendered SVG pixels | JSVG |
| 2 | [batik-transcoder](https://xmlgraphics.apache.org/batik/using/transcoder.html) | org.apache.xmlgraphics:batik-transcoder:1.20 | 11 | Rendered SVG pixels | Apache Batik SVG renderer, using batik-codec for PNG output |
| 3 | [batik-anim](https://xmlgraphics.apache.org/batik/using/dom-api.html) | org.apache.xmlgraphics:batik-anim:1.20 | 9 | SVG DOM dimensions and rectangle elements | Apache Batik SVG DOM |
| 4 | [batik-swing](https://xmlgraphics.apache.org/batik/using/swing.html) | org.apache.xmlgraphics:batik-swing:1.20 | 3 | SVG DOM dimensions and rectangle elements | Apache Batik SVG DOM and renderer via Swing canvas |
| 5 | [batik-svgrasterizer](https://xmlgraphics.apache.org/batik/javadoc/org/apache/batik/apps/rasterizer/SVGConverter.html) | org.apache.xmlgraphics:batik-svgrasterizer:1.20 | 2 | Rendered SVG pixels | Apache Batik SVG renderer via transcoder |
| 5 | [itext-svg](https://api.itextpdf.com/iText/java/9.8.0/com/itextpdf/svg/converter/SvgConverter.html) | com.itextpdf:svg:9.8.0 | 2 | SVG XObject dimensions | iText SVG parser and PDF renderer |
| 7 | [imageio-batik](https://github.com/haraldk/TwelveMonkeys#file-formats-supported) | com.twelvemonkeys.imageio:imageio-batik:3.15.2 | 0 | Rendered SVG pixels | TwelveMonkeys ImageIO wrapper over Apache Batik |
| 7 | [imageio-native-vips](https://github.com/ghosthack/imageio-native#optional-backends) | io.github.ghosthack:imageio-native-vips:2.0.0 | 0 | Rendered SVG pixels | imageio-native-vips wrapper over libvips SVG decoder |
| 7 | [jSVGIcon](https://github.com/BWeng20/jSVGIcon/blob/main/src/main/java/com/bw/jtools/svg/SVGConverter.java) | io.github.bweng20:jSVGIcon:1.6 | 0 | Rendered SVG pixels | BWeng20 jSVGIcon Java2D shape converter |
| 7 | [jairosvg](https://github.com/brunoborges/jairosvg#library-api) | io.brunoborges:jairosvg:1.0.16 | 0 | Rendered SVG pixels | JairoSVG Java2D SVG renderer |
| 7 | [svg-salamander](https://github.com/blackears/svgSalamander/blob/master/svg-core/src/main/java/com/kitfox/svg/SVGUniverse.java) | io.github.blackears:svg-salamander:1.1.5.5 | 0 | Rendered SVG pixels | SVG Salamander |
| unranked | [echosvg-anim](https://github.com/css4j/echosvg/blob/master/echosvg-anim/src/main/java/io/sf/carte/echosvg/anim/dom/SAXSVGDocumentFactory.java) | io.sf.carte:echosvg-anim:2.5 | unknown | SVG DOM dimensions and rectangle elements | EchoSVG SVG DOM (Apache Batik fork) |
| unranked | [echosvg-svgrasterizer](https://github.com/css4j/echosvg/blob/master/echosvg-svgrasterizer/src/main/java/io/sf/carte/echosvg/apps/rasterizer/SVGConverter.java) | io.sf.carte:echosvg-svgrasterizer:2.5 | unknown | Rendered SVG pixels | EchoSVG SVG renderer via rasterizer (Apache Batik fork) |
| unranked | [echosvg-swing](https://github.com/css4j/echosvg/blob/master/echosvg-swing/src/main/java/io/sf/carte/echosvg/swing/JSVGCanvas.java) | io.sf.carte:echosvg-swing:2.5 | unknown | SVG DOM dimensions and rectangle elements | EchoSVG SVG DOM and renderer via Swing (Apache Batik fork) |
| unranked | [echosvg-transcoder-svg](https://github.com/css4j/echosvg/blob/master/echosvg-transcoder-svg/src/main/java/io/sf/carte/echosvg/transcoder/image/PNGTranscoder.java) | io.sf.carte:echosvg-transcoder-svg:2.5 | unknown | Rendered SVG pixels | EchoSVG SVG renderer (Apache Batik fork) |
