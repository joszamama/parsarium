# symphonia-bundle-mp3 — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parser family:** Symphonia MP3 demuxer and decoder
- **Local input API:** `MpaReader::try_new(MediaSourceStream::new(Box::new(Cursor::new(bytes)), ..), FormatOptions::default()); FormatReader::next_packet(); MpaDecoder::try_new(params, ..).decode(&packet)`
- **Documentation:** [API reference](<https://docs.rs/symphonia-bundle-mp3/0.6.1/symphonia_bundle_mp3/>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../data/rust/mp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298,
  "decoded_frames": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 rust symphonia_bundle_mp3
python3 parsarium.py run mp3 rust symphonia_bundle_mp3 controls/mp3/tone-44k-mono.mp3
```
