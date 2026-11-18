# wuffs — PNG / C

- **Pinned release:** `0.3.6`
- **Upstream:** [source repository](<https://github.com/google/wuffs>)
- **License:** Apache-2.0
- **Parsed scope:** PNG image configuration
- **Underlying family:** Wuffs PNG decoder
- **Local input API:** `wuffs_png__decoder__decode_image_config(decoder, image_config*, io_buffer*) over local bytes`
- **Documentation:** [API reference](<https://github.com/google/wuffs/blob/v0.3.6/doc/std/image-decoders.md>)
- **Catalog evidence:** [parser record](../../../../data/c/png/parsers.json) · [control verification](../../../../data/c/png/verification.json) · [within-ecosystem ranking](../../../../data/c/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Independent generated-C PNG decoder. Control result covers parsed PNG image configuration (dimensions), not decoded pixels.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/wuffs/README.md)

```sh
python3 parsarium.py build png c wuffs
python3 parsarium.py run png c wuffs controls/png/red-green.png
```
