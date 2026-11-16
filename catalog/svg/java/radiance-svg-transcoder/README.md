# radiance-svg-transcoder — SVG / Java

- **Pinned release:** `7.5.0`
- **License:** BSD-3-Clause
- **Parsed scope:** Generated Java2D drawing code with SVG dimensions and colors
- **Underlying family:** Radiance SVG-to-Java2D transcoder using Apache Batik
- **Local input API:** `SvgStreamTranscoder(InputStream, String, LanguageRenderer).setPrintWriter(PrintWriter).transcode(InputStream template)`
- **Documentation:** [API reference](<https://github.com/kirill-grouchnikov/radiance/tree/master/tools/svg-transcoder>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "dimensions": true,
  "red": true,
  "green": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/radiance_svg_transcoder/README.md)

```sh
python3 parsarium.py build svg java radiance_svg_transcoder
python3 parsarium.py run svg java radiance_svg_transcoder controls/svg/red-green.svg
```
