# league/color-extractor — PNG / PHP

- **Pinned release:** `0.4.0`
- **License:** MIT
- **Parsed scope:** decoded pixel color histogram
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Palette::fromFilename(local PNG path); getMostUsedColors`
- **Documentation:** [API reference](<https://github.com/thephpleague/color-extractor/blob/21fcac6249c5ef7d00eb83e128743ee6678fe505/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "colors": {
    "#00ff00": 1,
    "#ff0000": 1
  }
}
```

Uses PHP GD imagecreatefromstring; verifies both control colors and counts.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/league_color_extractor/README.md)

```sh
python3 parsarium.py build png php league_color_extractor
python3 parsarium.py run png php league_color_extractor controls/png/red-green.png
```
