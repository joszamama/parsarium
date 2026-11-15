# boost-gil — ASCII PNM / C++

- **Pinned release:** `1.92.0`
- **License:** BSL-1.0
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** Boost.GIL native PNM reader
- **Local input API:** `boost::gil::read_image(filename, rgb8_image_t&, pnm_tag()); const_view(image)(x,y) channels`
- **Documentation:** [API reference](<https://www.boost.org/latest/libs/gil/doc/html/io.html>)
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

The Boost.GIL I/O documentation describes P1–P6 input; the committed control proves only P3. Its tag-pinned GIL parser source is compiled with exact-release installed Boost base headers.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
