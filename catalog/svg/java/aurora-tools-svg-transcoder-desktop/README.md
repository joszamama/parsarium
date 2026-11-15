# aurora-tools-svg-transcoder-desktop — SVG / Java

- **Pinned release:** `1.3.0`
- **License:** Apache-2.0
- **Parsed scope:** SVG DOM dimensions and rectangle elements after rendering tree construction
- **Underlying family:** Aurora SVG-to-Compose transcoder using Apache Batik
- **Local input API:** `SvgTranscoder(local file URI, String).setListener(...).transcode(InputStream template)`
- **Documentation:** [API reference](<https://github.com/kirill-grouchnikov/aurora/blob/icicle/tools/svg-transcoder/src/desktopMain/kotlin/org/pushingpixels/aurora/tools/svgtranscoder/SvgTranscoder.kt>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
