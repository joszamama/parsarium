# nanosvg — SVG / C

- **Pinned release:** `2023-12-29`
- **Upstream:** [source repository](<https://github.com/memononen/nanosvg>)
- **License:** Zlib
- **Parsed scope:** SVG root dimensions and two parsed rectangle shapes with paths
- **Underlying family:** NanoSVG native SVG parser
- **Local input API:** `nsvgParseFromFile(local SVG filename, "px", 96.0f); inspect NSVGimage shape/path lists`
- **Documentation:** [API reference](<https://github.com/memononen/nanosvg#parser>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "shapes": 2,
  "paths": 2
}
```

SDL3_image embeds NanoSVG; this direct C API is a distinct package path over the same parser family. Upstream has no tagged release; vcpkg publishes version-date 2023-12-29 pinned to the exact upstream commit.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/nanosvg/README.md)

```sh
python3 parsarium.py build svg c nanosvg
python3 parsarium.py run svg c nanosvg controls/svg/red-green.svg
```
