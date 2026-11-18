# JAVA × SVG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Direct dependents (deps.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jsvg](https://github.com/weisJ/jsvg) | 2.0.0 | 26 | Rendered SVG pixels | JSVG |
| 2 | [batik-transcoder](https://xmlgraphics.apache.org/batik/using/transcoder.html) | 1.20 | 11 | Rendered SVG pixels | Apache Batik SVG renderer, using batik-codec for PNG output |
| 3 | [batik-anim](https://xmlgraphics.apache.org/batik/using/dom-api.html) | 1.20 | 9 | SVG DOM dimensions and rectangle elements | Apache Batik SVG DOM |
| 4 | [fop-core](https://xmlgraphics.apache.org/fop/dev/svg.html) | 2.12 | 4 | PDF page dimensions and SVG-derived red/green drawing operations | Apache FOP SVG-to-PDF transcoder using Apache Batik |
| 5 | [batik-swing](https://xmlgraphics.apache.org/batik/using/swing.html) | 1.20 | 3 | SVG DOM dimensions and rectangle elements | Apache Batik SVG DOM and renderer via Swing canvas |
| 6 | [batik-svgrasterizer](https://xmlgraphics.apache.org/batik/javadoc/org/apache/batik/apps/rasterizer/SVGConverter.html) | 1.20 | 2 | Rendered SVG pixels | Apache Batik SVG renderer via transcoder |
| 7 | [gsvg](https://github.com/Alipsa/gsvg#readparse-an-existing-svg-file-and-change-it) | 1.2.0 | 2 | Typed SVG dimensions, rectangle elements, and fill attributes | gsvg typed SVG model (Groovy library callable from Java) |
| 8 | [itext-svg](https://api.itextpdf.com/iText/java/9.8.0/com/itextpdf/svg/converter/SvgConverter.html) | 9.8.0 | 2 | SVG XObject dimensions | iText SVG parser and PDF renderer |
| 9 | [aurora-tools-svg-transcoder-desktop](https://github.com/kirill-grouchnikov/aurora/blob/icicle/tools/svg-transcoder/src/desktopMain/kotlin/org/pushingpixels/aurora/tools/svgtranscoder/SvgTranscoder.kt) | 1.3.0 | 1 | SVG DOM dimensions and rectangle elements after rendering tree construction | Aurora SVG-to-Compose transcoder using Apache Batik |
| 10 | [radiance-svg-transcoder](https://github.com/kirill-grouchnikov/radiance/tree/master/tools/svg-transcoder) | 7.5.0 | 1 | Generated Java2D drawing code with SVG dimensions and colors | Radiance SVG-to-Java2D transcoder using Apache Batik |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
