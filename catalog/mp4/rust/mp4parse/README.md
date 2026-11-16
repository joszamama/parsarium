# mp4parse — MP4 / Rust

- **Pinned release:** `0.17.0`
- **License:** MPL-2.0
- **Parsed scope:** ISO-BMFF movie track table
- **Underlying family:** Mozilla mp4parse
- **Local input API:** `read_mp4(&mut File).tracks`
- **Documentation:** [API reference](<https://docs.rs/mp4parse/0.17.0/mp4parse/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4parse/README.md)

```sh
python3 parsarium.py build mp4 rust mp4parse
python3 parsarium.py run mp4 rust mp4parse controls/mp4/red-av.mp4
```
