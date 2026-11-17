# minimp3 — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.6.1`
- **License:** MIT (minimp3 and minimp3-sys 0.6.0 Rust crates); CC0-1.0 (vendored minimp3.h)
- **Parser family:** lieff/minimp3 C decoder via minimp3-sys 0.6.0 Rust FFI binding
- **Local input API:** `minimp3::Decoder::new(std::io::Cursor<&[u8]>); Decoder::next_frame() -> Frame { data: Vec<i16>, sample_rate, channels, layer, bitrate } until Error::Eof`
- **Documentation:** [API reference](<https://docs.rs/minimp3/0.6.1/minimp3/>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../projects/mp3/rust/minimp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "layer": 3,
  "bitrate_kbps": 64,
  "frames": 11,
  "samples_per_channel": 12672,
  "pcm_samples": 12672,
  "pcm_sha256": "0641e37cb18148b29cfc23ffc8c479115a4e042a0952a91570e92888aec0a33e"
}
```

## Run this target

```sh
python3 parsarium.py build mp3 rust minimp3
python3 parsarium.py run mp3 rust minimp3 controls/mp3/tone-44k-mono.mp3
```
