# revelo-parsers-container — MP4 / Rust

- **Pinned release:** `0.5.6`
- **License:** BSD-2-Clause
- **Parsed scope:** MP4 audio and video stream graph
- **Underlying family:** Revelo MP4 parser
- **Local input API:** `parse_mp4(&mut FileAnalyze::new(&bytes)); stream_count()`
- **Documentation:** [API reference](<https://docs.rs/revelo-parsers-container/0.5.6/revelo_parsers_container/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_streams": 1,
  "audio_streams": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/revelo_parsers_container/README.md)

```sh
python3 parsarium.py build mp4 rust revelo_parsers_container
python3 parsarium.py run mp4 rust revelo_parsers_container controls/mp4/red-av.mp4
```
