# bwavfile — WAV / Rust

- **Pinned release:** `2.0.1`
- **License:** MIT
- **Parsed scope:** WAV format and declared frame length
- **Underlying family:** bwavfile reader
- **Local input API:** `WaveReader::open(path).format().frame_length()`
- **Documentation:** [API reference](<https://docs.rs/bwavfile/2.0.1/bwavfile/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/bwavfile/README.md)

```sh
python3 parsarium.py build wav rust bwavfile
python3 parsarium.py run wav rust bwavfile controls/wav/four-samples.wav
```
