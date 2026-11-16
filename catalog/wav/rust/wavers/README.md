# wavers — WAV / Rust

- **Pinned release:** `1.5.1`
- **License:** MIT
- **Parsed scope:** Decoded PCM sample values and WAV metadata
- **Underlying family:** wavers reader
- **Local input API:** `read::<i16,_>(path); Wav::from_path(path)`
- **Documentation:** [API reference](<https://docs.rs/wavers/1.5.1/wavers/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/wavers/README.md)

```sh
python3 parsarium.py build wav rust wavers
python3 parsarium.py run wav rust wavers controls/wav/four-samples.wav
```
