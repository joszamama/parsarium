# bitandblack/image-information — SVG / PHP

- **Pinned release:** `3.3.0`
- **License:** MIT
- **Parsed scope:** SVG dimension reader only; PECL Imagick 3.8.1 parses via ImageMagick delegate.
- **Underlying family:** ImageMagick SVG reader via PECL Imagick
- **Local input API:** `Image(new Source\File(local SVG path))->getSize invokes SVG image type reader through PECL Imagick`
- **Documentation:** [API reference](<https://bitbucket.org/wirbelwild/imageinformation/src/26a850670d6858740db1a506cb2197a5393e43c5/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Composer package wraps a PECL Imagick SVG reader; pinned extension source is data/php/ascii_pnm/pecl-imagick-lock.json.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/bitandblack_image_information/README.md)

```sh
python3 parsarium.py build svg php bitandblack_image_information
python3 parsarium.py run svg php bitandblack_image_information controls/svg/red-green.svg
```
