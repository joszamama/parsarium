# openimageio — PNG / C++

- **Pinned release:** `3.2.2.0`
- **License:** Apache-2.0
- **Parsed scope:** RGBA pixels
- **Underlying family:** OpenImageIO PNG ImageInput plugin over linked libpng
- **Local input API:** `OIIO::ImageInput::open(local PNG filename) and read_image(..., OIIO::TypeDesc::UINT8, buffer) return dimensions and RGBA pixels`
- **Documentation:** [API reference](<https://openimageio.readthedocs.io/en/v3.2.2.0/imageinput.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

The pinned OpenImageIO dylib links Homebrew libpng 1.6.59. This is a distinct C++ ImageInput API sharing libpng as its PNG syntax engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
