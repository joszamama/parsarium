# rockbox-metadata — MP4 / Rust

- **Pinned release:** `0.1.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MP4 audio title and sample rate
- **Underlying family:** Rockbox C metadata parser binding
- **Local input API:** `read(path).title/sample_rate`
- **Documentation:** [API reference](<https://docs.rs/rockbox-metadata/0.1.1/rockbox_metadata/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "sample_rate": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/rockbox_metadata/README.md)

```sh
python3 parsarium.py build mp4 rust rockbox_metadata
python3 parsarium.py run mp4 rust rockbox_metadata controls/mp4/red-av.mp4
```
