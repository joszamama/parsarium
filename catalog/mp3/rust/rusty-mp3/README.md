# rusty_mp3 — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.6`
- **License:** Apache-2.0
- **Parser family:** rusty_mp3 pure-Rust Layer III decoder (remade_ffmpeg_rs)
- **Local input API:** `rusty_mp3::Mp3Decoder::new(); Mp3Decoder::push(&bytes); Mp3Decoder::flush(); Mp3Decoder::next_frame() -> DecodedAudio { sample_rate, channels, samples: Vec<f32> } until Error::Eof`
- **Documentation:** [API reference](<https://docs.rs/rusty_mp3/1.0.6/rusty_mp3/struct.Mp3Decoder.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../projects/mp3/rust/rusty_mp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "samples_per_channel": 12672,
  "pcm_samples": 12672,
  "pcm_f32_sha256": "950a4b2c13148eef937e478e683959d5450f71436c95e81423456a85b63dfb8a"
}
```

## Verification scope

Both untagged valid controls give 11 frames at 44,100 Hz mono and 12 frames at 22,050 Hz stereo, 12,672 and 6,912 samples per channel, equal to the independent header walk (11 x 1152 and 12 x 576) and to the Symphonia receipts. Mp3Decoder drops a frame whose decode fails without reporting it, so the frame count is checked against the walk rather than trusted. Docker LLVM coverage: 1121 own crate lines on the first control (decoder, header, side information, Huffman, IMDCT, synthesis; encoder files 0). AFL++ SanitizerCoverage is scoped to the rusty_mp3 crate: 1082 vs 1033 tuples, 219 and 170 unique, byte-identical maps over 5 separate processes per control. Two short CBR controls do not establish VBR, Xing/Info, free-format or MPEG-2.5 support; no malformed, resource-use or campaign tests were run.

## Run this target

```sh
python3 parsarium.py build mp3 rust rusty_mp3
python3 parsarium.py run mp3 rust rusty_mp3 controls/mp3/tone-44k-mono.mp3
```
