# stb — PNG / C++

- **Pinned release:** `cci.20261021`
- **License:** MIT OR Unlicense
- **Parsed scope:** pixels
- **Underlying family:** stb_image
- **Local input API:** `stbi_load(const char* filename, int*, int*, int*, int) from stb_image.h`
- **Documentation:** [API reference](<https://github.com/nothings/stb/blob/a7d4c2175630e1ea5b6f8dd00ab96fed0b97b96d/stb_image.h>)
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

Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/stb/README.md)

```sh
python3 parsarium.py build png cpp stb
python3 parsarium.py run png cpp stb controls/png/red-green.png
```
