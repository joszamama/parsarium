# surge-hound — WAV / Rust

- **Pinned release:** `0.2.11-alpha.0`
- **License:** Apache-2.0
- **Parsed scope:** Decoded PCM sample values and WAV metadata
- **Underlying family:** Hound fork (surge-hound)
- **Local input API:** `WavReader::open(path).samples::<i16>()`
- **Documentation:** [API reference](<https://docs.rs/surge-hound/0.2.11-alpha.0/surge_hound/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/surge_hound/README.md)

```sh
python3 parsarium.py build wav rust surge_hound
python3 parsarium.py run wav rust surge_hound controls/wav/four-samples.wav
```
