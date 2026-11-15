# qtwebengine — SVG / C++

- **Pinned release:** `6.11.2`
- **License:** LGPL-3.0-only
- **Parsed scope:** parsed SVG DOM root, dimensions and two rectangle elements
- **Underlying family:** QtWebEngine over Chromium Blink SVG DOM parser
- **Local input API:** `QWebEnginePage::load(QUrl::fromLocalFile(local filename)); loadFinished; runJavaScript(document.documentElement and querySelectorAll)`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qwebenginepage.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "root": "svg",
  "width": 2,
  "height": 1,
  "rectangles": 2
}
```

The QtWebEngine package embeds Chromium Blink; the adapter reads SVG-specific DOM elements from a local SVG document, distinct from QtSvg and QtDeclarative VectorImage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
