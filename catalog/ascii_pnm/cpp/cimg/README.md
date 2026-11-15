# cimg — ASCII PNM / C++

- **Pinned release:** `4.0.5`
- **License:** CeCILL-C-1.0 OR CeCILL-2.1
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels when maxval shares the dimensions line
- **Underlying family:** CImg native PNM reader
- **Local input API:** `cimg_library::CImg<unsigned char>::get_load_pnm(const char* filename); width(), height(), and pixel(x,y,0,channel)`
- **Documentation:** [API reference](<https://cimg.eu/reference/structcimg__library_1_1CImg.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green-inline.ppm`](../../../../controls/ascii_pnm/red-green-inline.ppm)

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

CImg 4.0.5 misreads the original valid P3 control whose maxval occupies a separate line; a second valid P3 control with dimensions and maxval on the same line is used, and the limitation is not generalized to all P3 layouts.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
