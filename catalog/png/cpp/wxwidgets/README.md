# wxwidgets — PNG / C++

- **Pinned release:** `3.3.4`
- **License:** LGPL-2.0-or-later WITH WxWindows-exception-3.1
- **Parsed scope:** RGB pixels
- **Underlying family:** wxWidgets wxPNGHandler over linked libpng
- **Local input API:** `wxImage::AddHandler(new wxPNGHandler), wxImage::LoadFile(local PNG filename, wxBITMAP_TYPE_PNG), then GetWidth/GetHeight/GetRed/GetGreen/GetBlue`
- **Documentation:** [API reference](<https://github.com/wxWidgets/wxWidgets/blob/v3.3.4/include/wx/image.h>)
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
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

The pinned wxWidgets core dylib links Homebrew libpng 1.6.59. Its image handler exposes a distinct C++ API over the same underlying PNG decoder. The valid RGBA control returned RGB values; this run did not observe alpha data through wxImage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
