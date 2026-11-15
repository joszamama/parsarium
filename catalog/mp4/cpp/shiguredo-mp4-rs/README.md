# shiguredo-mp4-rs — MP4 / C++

- **Pinned release:** `2026.3.0`
- **License:** Apache-2.0
- **Parsed scope:** Two parsed MP4 tracks (one video, one audio) and one-second video duration
- **Underlying family:** shiguredo/mp4-rs Rust ISO BMFF demuxer through its published C API
- **Local input API:** `mp4_file_demuxer_get_required_input; mp4_file_demuxer_handle_input(local FILE bytes); mp4_file_demuxer_get_tracks`
- **Documentation:** [API reference](<https://github.com/shiguredo/mp4-rs/blob/2026.3.0/crates/c-api/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video_tracks": 1,
  "audio_tracks": 1,
  "video_duration_ms": 1000
}
```

The C and C++ adapters link the same tagged Rust static library and call its published C API; one underlying parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
