# pngtools — PNG / Python

- **Pinned release:** `1.0.2`
- **License:** MIT
- **Parsed scope:** chunks
- **Underlying family:** pngtools chunk parser
- **Local input API:** `pngtools.read_file(local path); get_type_of_chunk`
- **Documentation:** [API reference](<https://github.com/its-just-nans/pngtools/blob/main/pngtools/lib.py>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "chunks": [
    "IHDR",
    "IDAT",
    "IEND"
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/pngtools/README.md)

```sh
python3 parsarium.py build png python pngtools
python3 parsarium.py run png python pngtools controls/png/red-green.png
```
