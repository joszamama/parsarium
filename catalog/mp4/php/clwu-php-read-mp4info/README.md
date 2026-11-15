# clwu/php-read-mp4info — MP4 / PHP

- **Pinned release:** `v2.0.0`
- **License:** BSD-3-Clause
- **Parsed scope:** 2 × 2 video track and zero-degree rotation
- **Underlying family:** Clwu native PHP MP4 atom parser
- **Local input API:** `Mp4::getInfo(local MP4 path); parsed video track width, height, and rotation`
- **Documentation:** [API reference](<https://github.com/clwu88/php-read-mp4info/blob/286726a66ce6e743f1de118557ce1528645fe106/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "rotate": 0
}
```

Own PHP MP4 box/track-header parser; reads dimensions and transform matrix.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
