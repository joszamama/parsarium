# nanomp3 — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parser family:** minimp3 decoder family via the nanomp3-core 0.2.0 pure-Rust port
- **Local input API:** `nanomp3::frames(&bytes) -> Frame { data, channels, sample_rate, layer, bitrate_kbps, samples }; nanomp3::decode_all::<i16>(&bytes) and nanomp3::decode_all_with::<i16>(&bytes, Options::default().minimp3_compat(true)) -> Decoded { samples, channels, sample_rate, layer, .. }`
- **Documentation:** [API reference](<https://docs.rs/nanomp3/0.2.0/nanomp3/fn.decode_all.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../projects/mp3/rust/nanomp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "layer": 3,
  "bitrate_kbps": 64,
  "frames": 11,
  "frame_bytes": 2298,
  "frame_samples_per_channel": 12672,
  "samples_per_channel": 12672,
  "pcm_samples": 12672,
  "pcm_sha256": "1106d468c6a515a4c554991af6ab95e9c811e8e34005478ee81dd1e3a8063edb",
  "minimp3_compat_pcm_sha256": "d8bde33ad59477f815f1194dd04517bf8b5949807f5bf01fb19a9ab4e3a99364"
}
```

## Verification scope

Both untagged valid controls give 11 frames/2,298 bytes at 44,100 Hz mono 64 kbps and 12 frames/1,254 bytes at 22,050 Hz stereo 32 kbps, 12,672 and 6,912 samples per channel, equal to the independent header walk and the minimp3 and Symphonia receipts. No LAME/Xing tag is present, so decode_all trims no delay or padding. Docker LLVM coverage: 164 own nanomp3 lines and 985 underlying nanomp3-core lines on the first control. AFL++ SanitizerCoverage is scoped to nanomp3, nanomp3-core and the harness crate, where the generic i16 loader and frame decoder are monomorphized: 955 vs 990 tuples, 97 and 132 unique, byte-identical maps over 5 separate processes per control. Two short CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II or MPEG-2.5 support; no malformed, resource-use or campaign tests were run.

## Run this target

```sh
python3 parsarium.py build mp3 rust nanomp3
python3 parsarium.py run mp3 rust nanomp3 controls/mp3/tone-44k-mono.mp3
```
