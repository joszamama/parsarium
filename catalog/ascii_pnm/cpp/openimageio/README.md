# openimageio — ASCII PNM / C++

- **Pinned release:** `3.2.2.0`
- **Upstream:** [source repository](<https://github.com/AcademySoftwareFoundation/OpenImageIO>) · [Debian](<https://tracker.debian.org/pkg/openimageio>)
- **License:** Apache-2.0
- **Parsed scope:** P3 format identification, ASCII encoding flag, dimensions, and two decoded RGB pixels
- **Underlying family:** OpenImageIO native PNM plugin
- **Local input API:** `OIIO::ImageInput::open(localPath); spec(); read_image(0,0,0,nchannels, span<uint8_t>)`
- **Documentation:** [API reference](<https://openimageio.readthedocs.io/en/v3.2.2.0/imageinput.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "pnm",
  "binary": 0,
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

ImageInput opens the local P3 file through the OpenImageIO PNM plugin; the image spec identifies ASCII encoding and decoded RGB pixels. Repository stars measure the whole multi-format library.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/cpp/openimageio/README.md)

```sh
python3 parsarium.py build ascii_pnm cpp openimageio
python3 parsarium.py run ascii_pnm cpp openimageio controls/ascii_pnm/red-green.ppm
```
