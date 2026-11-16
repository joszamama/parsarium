# oxideav-mp4 — MP4 / Rust

- **Pinned release:** `0.0.11`
- **License:** MIT
- **Parsed scope:** MP4 audio and video streams
- **Underlying family:** OxideAV MP4 demuxer
- **Local input API:** `register(RuntimeContext); open_demuxer("mp4", File).streams()`
- **Documentation:** [API reference](<https://docs.rs/oxideav-mp4/0.0.11/oxideav_mp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "streams": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/oxideav_mp4/README.md)

```sh
python3 parsarium.py build mp4 rust oxideav_mp4
python3 parsarium.py run mp4 rust oxideav_mp4 controls/mp4/red-av.mp4
```
