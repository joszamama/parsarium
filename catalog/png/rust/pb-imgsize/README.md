# pb-imgsize — PNG / Rust

- **Pinned release:** `0.2.5`
- **License:** MIT
- **Parsed scope:** PNG IHDR dimensions
- **Underlying family:** pb-imgsize PNG metadata reader
- **Local input API:** `read_bytes(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/pb-imgsize/0.2.5/pb_imgsize/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/rust/pb_imgsize/README.md)

```sh
python3 parsarium.py build png rust pb_imgsize
python3 parsarium.py run png rust pb_imgsize controls/png/red-green.png
```
