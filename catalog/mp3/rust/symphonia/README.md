# symphonia — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parser family:** Symphonia MP3 demuxer and decoder
- **Local input API:** `symphonia::default::get_probe().probe(&Hint::new(), MediaSourceStream::new(Box::new(Cursor::new(bytes)), ..), FormatOptions::default(), MetadataOptions::default()); FormatReader::next_packet(); symphonia::default::get_codecs().make_audio_decoder(params, ..).decode(&packet)`
- **Documentation:** [API reference](<https://docs.rs/symphonia/0.6.1/symphonia/>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../projects/mp3/rust/symphonia/verification.json)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3",
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298,
  "decoded_frames": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 rust symphonia
python3 parsarium.py run mp3 rust symphonia controls/mp3/tone-44k-mono.mp3
```
