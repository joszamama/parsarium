# wxwidgets — ASCII PNM / C++

- **Pinned release:** `3.3.4`
- **License:** LGPL-2.0-or-later WITH WxWindows-exception-3.1
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** wxWidgets native PNM handler
- **Local input API:** `wxImage::AddHandler(new wxPNMHandler); wxImage::LoadFile(path, wxBITMAP_TYPE_PNM); GetData()`
- **Documentation:** [API reference](<https://wxwidgets.org/docs/book/Cross-Platform%20GUI%20Programming%20with%20wxWidgets.pdf>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

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

wxPNMHandler reads ASCII PNM through wxImage; pinned 3.3.4 core and base libraries are checked by SHA-256. The project handles many other formats, so repository stars are only a broad adoption proxy.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
