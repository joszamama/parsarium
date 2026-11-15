# qtdeclarative — SVG / C++

- **Pinned release:** `6.12.0`
- **License:** LGPL-3.0-only
- **Parsed scope:** SVG vector scene loaded with parsed intrinsic dimensions
- **Underlying family:** Qt Quick VectorImage over QtSvg SVG document parser
- **Local input API:** `QQmlComponent creates QtQuick.VectorImage; source=QUrl::fromLocalFile(local filename); status and implicitWidth/implicitHeight`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qml-qtquick-vectorimage-vectorimage.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "ready": true
}
```

QtDeclarative VectorImage builds a Qt Quick scene from the QtSvg document/visitor parser. It is a separate package API sharing the QtSvg syntax engine with QtSvg and QtBase QImageReader.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
