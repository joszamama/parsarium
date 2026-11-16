# creak — WAV / Rust

- **Pinned release:** `0.3.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded PCM sample count and WAV metadata
- **Underlying family:** Hound WAV reader
- **Local input API:** `Decoder::open(path).into_samples()`
- **Documentation:** [API reference](<https://docs.rs/creak/0.3.0/creak/>)
- **Catalog evidence:** [parser record](../../../../data/rust/wav/parsers.json) · [control verification](../../../../data/rust/wav/verification.json) · [within-ecosystem ranking](../../../../data/rust/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": 4
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/rust/creak/README.md)

```sh
python3 parsarium.py build wav rust creak
python3 parsarium.py run wav rust creak controls/wav/four-samples.wav
```
