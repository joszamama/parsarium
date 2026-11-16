# batik-transcoder — SVG / Java

- **Pinned release:** `1.20`
- **License:** Apache-2.0
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** Apache Batik SVG renderer, using batik-codec for PNG output
- **Local input API:** `PNGTranscoder.transcode(TranscoderInput(InputStream), TranscoderOutput(OutputStream))`
- **Documentation:** [API reference](<https://xmlgraphics.apache.org/batik/using/transcoder.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/batik_transcoder/README.md)

```sh
python3 parsarium.py build svg java batik_transcoder
python3 parsarium.py run svg java batik_transcoder controls/svg/red-green.svg
```
