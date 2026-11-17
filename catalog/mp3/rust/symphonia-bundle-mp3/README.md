# symphonia-bundle-mp3 — MP3 / Rust

| | |
| --- | --- |
| Release | `0.6.1`, crates.io SHA-256 `98ea5ffc8716bff677dfb3b01b420c7b758de901a72b8c330bf2040ab74b4add` |
| License | MPL-2.0 |
| Source | [pdeljanov/Symphonia](https://github.com/pdeljanov/Symphonia/tree/v0.6.1/symphonia-bundle-mp3) |
| Documentation | [docs.rs](https://docs.rs/symphonia-bundle-mp3/0.6.1/symphonia_bundle_mp3/) |
| Input API | `MpaReader::try_new(MediaSourceStream::new(Box::new(Cursor::new(bytes)), ..), FormatOptions::default())`, `next_packet()`, `MpaDecoder::try_new(params, ..).decode(&packet)` |
| Family | Symphonia MP3 demuxer and decoder |
| Adoption | 10,651,437 crates.io recent downloads (90 days), 2026-11-17 |

## Control result

The harness passes the bytes of `controls/mp3/tone-44k-mono.mp3` to the reader from memory, with no temporary file. It reads every packet and decodes each one.

```json
{"sample_rate": 44100, "channels": 1, "frames": 11, "frame_bytes": 2298, "decoded_frames": 12672}
```

There are 11 packets, one per MPEG-1 Layer III frame. Their bytes sum to the file size, and 11 × 1,152 = 12,672 decoded samples per channel. `controls/mp3/check_controls.py` reads the frame headers independently and gives the same frame count and byte total.

The fixed second control, `tone-22k-stereo.mp3`, gives `{"sample_rate": 22050, "channels": 2, "frames": 12, "frame_bytes": 1254, "decoded_frames": 6912}` (12 × 576).

## Limits

The two controls are CBR Layer III files with no Xing/Info frame, so gapless trimming and VBR seeking are not exercised. MPEG-2.5, Layer I/II, and free-format streams are untested.

The afl.rs build instruments the whole fuzz binary, including symphonia-core, serde_json, and the harness, so the edge counts are not parser-only. The AFL++ receipt shows that the two controls produce different parser behavior. Each control gives the same edges on all three repeats (1,456 and 1,500). Each control also has edges the other lacks (116 and 160). Six symphonia-bundle-mp3 source files are covered differently, including `layer3/stereo.rs`, which only the stereo control reaches.
