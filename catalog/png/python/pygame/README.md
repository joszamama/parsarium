# pygame — PNG / Python

- **Pinned release:** `2.6.1`
- **License:** LGPL
- **Parsed scope:** pixels
- **Underlying family:** SDL_image/libpng
- **Local input API:** `pygame.image.load(local path).get_at`
- **Documentation:** [API reference](<https://www.pygame.org/docs/ref/image.html>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba0": [
    255,
    0,
    0,
    255
  ],
  "rgba1": [
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/pygame/README.md)

```sh
python3 parsarium.py build png python pygame
python3 parsarium.py run png python pygame controls/png/red-green.png
```
