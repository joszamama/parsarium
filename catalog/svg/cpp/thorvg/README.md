# thorvg — SVG / C++

- **Pinned release:** `1.1.3`
- **Upstream:** [source repository](<https://github.com/thorvg/thorvg>) · [Debian](<https://tracker.debian.org/pkg/thorvg>)
- **License:** MIT
- **Parsed scope:** parsed SVG document dimensions
- **Underlying family:** ThorVG SVG loader and native vector engine
- **Local input API:** `tvg::Initializer::init; tvg::Picture::gen; Picture::load(local filename); Picture::size`
- **Documentation:** [API reference](<https://github.com/thorvg/thorvg/blob/v1.1.3/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

ThorVG C binding and native C++ API are distinct ecosystem call paths over the same ThorVG SVG loader; they do not represent independent syntax engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/cpp/thorvg/README.md)

```sh
python3 parsarium.py build svg cpp thorvg
python3 parsarium.py run svg cpp thorvg controls/svg/red-green.svg
```
