# transcoder-core — SVG / Java

- **Pinned release:** `0.1.1`
- **License:** Apache-2.0
- **Parsed scope:** Generated Java drawing code with SVG dimensions and colors
- **Underlying family:** AndroidSvgTranscoder SVG-to-Java source using Apache Batik
- **Local input API:** `SvgTranscoder(local file URL, String).setExternalPrintWriter(PrintWriter).transcode()`
- **Documentation:** [API reference](<https://github.com/furutuki/AndroidSvgTranscoder#project-structure>)
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

[Docker harness and verification receipt](../../../../projects/svg/java/transcoder_core/README.md)

```sh
python3 parsarium.py build svg java transcoder_core
python3 parsarium.py run svg java transcoder_core controls/svg/red-green.svg
```
