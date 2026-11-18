# probe-image-size — PNG / JavaScript

- **Pinned release:** `7.5.0`
- **Upstream:** [source repository](<https://github.com/nodeca/probe-image-size>) · [npm](<https://www.npmjs.com/package/probe-image-size>)
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** probe-image-size
- **Local input API:** `probe.sync(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/probe-image-size>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": "png"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/probe_image_size/README.md)

```sh
python3 parsarium.py build png javascript probe_image_size
python3 parsarium.py run png javascript probe_image_size controls/png/red-green.png
```
