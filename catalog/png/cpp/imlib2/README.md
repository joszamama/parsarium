# imlib2 — PNG / C++

- **Pinned release:** `1.12.7`
- **Upstream:** [source repository](<https://sourceforge.net/projects/enlightenment/>) · [Debian](<https://tracker.debian.org/pkg/imlib2>)
- **License:** Imlib2
- **Parsed scope:** pixels
- **Underlying family:** Imlib2 PNG loader (libpng-backed)
- **Local input API:** `imlib_load_image_immediately(const char* file); imlib_image_get_data_for_reading_only()`
- **Documentation:** [API reference](<https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/>)
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

The pinned source release includes the documented Imlib2.h.in C API and a PNG loader module. Primary Enlightenment repository is not GitHub. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/imlib2/README.md)

```sh
python3 parsarium.py build png cpp imlib2
python3 parsarium.py run png cpp imlib2 controls/png/red-green.png
```
