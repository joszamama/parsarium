# pyvips — PNG / Python

- **Pinned release:** `3.2.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** libvips PNG
- **Local input API:** `pyvips.Image.new_from_file(local path).write_to_memory()`
- **Documentation:** [API reference](<https://libvips.github.io/pyvips/vimage.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
