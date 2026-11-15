# jply — ASCII PLY / Java

- **Pinned release:** `0.2.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex and face counts, parsed face indices
- **Underlying family:** jPLY native PLY element reader
- **Local input API:** `new PlyReaderFile(File local path), nextElementReader(), readElement()`
- **Documentation:** [API reference](<https://github.com/smurn/jPLY>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "indices": [
    0,
    1,
    2
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/jply/README.md)

```sh
python3 parsarium.py build ascii_ply java jply
python3 parsarium.py run ascii_ply java jply controls/ascii_ply/triangle.ply
```
