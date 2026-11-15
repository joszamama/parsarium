# echosvg-transcoder-svg — SVG / Java

- **Pinned release:** `2.5`
- **License:** Apache-2.0
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** EchoSVG SVG renderer (Apache Batik fork)
- **Local input API:** `PNGTranscoder.transcode(TranscoderInput(InputStream), TranscoderOutput(OutputStream))`
- **Documentation:** [API reference](<https://github.com/css4j/echosvg/blob/master/echosvg-transcoder-svg/src/main/java/io/sf/carte/echosvg/transcoder/image/PNGTranscoder.java>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
