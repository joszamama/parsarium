# juce — SVG / C++

- **Pinned release:** `9.0.5`
- **License:** AGPL-3.0-only
- **Parsed scope:** parsed SVG drawable bounds from local file
- **Underlying family:** JUCE juce_graphics over bundled LunaSVG
- **Local input API:** `juce::Drawable::createFromSVGFile(juce::File(local filename)); getDrawableBounds()`
- **Documentation:** [API reference](<https://docs.juce.com/develop/classjuce_1_1Drawable.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

JUCE SVGParser.cpp calls bundled LunaSVG and converts its document to a JUCE Drawable tree; this shares the LunaSVG parser family with the direct LunaSVG row.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
