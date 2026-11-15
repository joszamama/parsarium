# rply — ASCII PLY / C

- **Pinned release:** `1.1.4`
- **License:** MIT
- **Parsed scope:** three vertex callbacks and three face-index callbacks from ASCII PLY
- **Underlying family:** RPly 1.1.4 ANSI C parser
- **Local input API:** `ply_open(local filename); ply_read_header; ply_set_read_cb; ply_read`
- **Documentation:** [API reference](<https://w3.impa.br/~diego/software/rply/>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

C and C++ adapters link the same pinned RPly C core; the C++ adapter calls its documented extern C API.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/rply/README.md)

```sh
python3 parsarium.py build ascii_ply c rply
python3 parsarium.py run ascii_ply c rply controls/ascii_ply/triangle.ply
```
