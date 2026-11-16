# lodepng — PNG / C

- **Pinned release:** `cci.20260102`
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** LodePNG
- **Local input API:** `lodepng_decode32_file(unsigned char**, unsigned*, unsigned*, const char*)`
- **Documentation:** [API reference](<https://github.com/lvandeve/lodepng/blob/865adac2b8149774401626101ec618e3de45e1d8/lodepng.h>)
- **Catalog evidence:** [parser record](../../../../data/c/png/parsers.json) · [control verification](../../../../data/c/png/verification.json) · [within-ecosystem ranking](../../../../data/c/png/ranking.md)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/lodepng/README.md)

```sh
python3 parsarium.py build png c lodepng
python3 parsarium.py run png c lodepng controls/png/red-green.png
```
