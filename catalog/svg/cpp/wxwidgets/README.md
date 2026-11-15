# wxwidgets — SVG / C++

- **Pinned release:** `3.3.4`
- **License:** LGPL-2.0-or-later WITH WxWindows-exception-3.1
- **Parsed scope:** SVG dimensions and two rendered RGB pixels
- **Underlying family:** wxWidgets wxBitmapBundle over bundled NanoSVG
- **Local input API:** `wxBitmapBundle::FromSVGFile(local filename, wxSize); GetBitmap; ConvertToImage`
- **Documentation:** [API reference](<https://github.com/wxWidgets/wxWidgets/blob/v3.3.4/include/wx/bmpbndl.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

This Homebrew wxWidgets build defines wxUSE_NANOSVG=1, wxUSE_NANOSVG_EXTERNAL=0 and wxUSE_LUNASVG=0. It embeds NanoSVG, sharing that syntax parser family with SDL3_image.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
