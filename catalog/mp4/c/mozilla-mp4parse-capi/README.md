# mozilla-mp4parse-capi — MP4 / C

- **Pinned release:** `0.17.0`
- **License:** MPL-2.0
- **Parsed scope:** MP4 track count, video/audio track types and video display dimensions
- **Underlying family:** Mozilla mp4parse Rust ISO BMFF parser through published C API
- **Local input API:** `Mp4parseIo read callback over local FILE*; mp4parse_new; mp4parse_get_track_count; mp4parse_get_track_info; mp4parse_get_track_video_info`
- **Documentation:** [API reference](<https://docs.rs/mp4parse_capi/0.17.0/mp4parse_capi/>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video": 1,
  "audio": 1,
  "width": 2,
  "height": 2
}
```

The published mp4parse_capi crate uses Mozilla mp4parse 0.17.0 for syntax interpretation; no other accepted C MP4 package path in this cell shares this parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
