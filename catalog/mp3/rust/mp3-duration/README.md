# mp3-duration — MP3 / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.10`
- **License:** MIT
- **Parser family:** mp3-duration Rust MPEG frame-header scanner
- **Local input API:** `mp3_duration::from_read(&mut std::io::Cursor<&[u8]>) -> Result<std::time::Duration, MP3DurationError>`
- **Documentation:** [API reference](<https://docs.rs/mp3-duration/0.1.10/mp3_duration/fn.from_read.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control result](../../../../projects/mp3/rust/mp3_duration/verification.json)

## Observed control result

```json
{
  "duration_ns": 287346928
}
```

## Verification scope

Both untagged valid controls return 287,346,928 ns and 313,469,376 ns, equal to the independent header walk in controls/mp3/check_controls.py: 11 MPEG-1 frames x floor(1152e9/44100) ns and 12 MPEG-2 frames x floor(576e9/22050) ns. The API exposes no frame count, so the frame count is checked only through that product. Docker LLVM coverage: 122 own crate lines on the first control. AFL++ SanitizerCoverage is scoped to mp3_duration and the harness crate, where the generic from_read::<Cursor<&[u8]>> is monomorphized: 77 vs 77 tuples, 1 unique to each control, byte-identical maps over 5 separate processes per control. Covered line sets differ by two src/lib.rs lines each way (MPEG-1 vs MPEG-2 version arm, mono vs joint-stereo mode arm). The feedback differential is real but small, because the per-frame work is table-driven. Two short CBR controls do not establish VBR, Xing/Info, free-format or other layer support; no malformed, resource-use or campaign tests were run.
