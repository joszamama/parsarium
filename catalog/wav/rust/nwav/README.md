# nwav — WAV / Rust

- **Pinned release:** `0.1.2`
- **License:** MIT
- **Parsed scope:** WAV fmt/data chunks and declared sample count
- **Underlying family:** nwav chunk reader
- **Local input API:** `WAV::from_data(&[u8]).read_chunk_by_name("fmt ")`
- **Documentation:** [API reference](<https://docs.rs/nwav/0.1.2/nwav/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/nwav/README.md)

```sh
python3 parsarium.py build wav rust nwav
python3 parsarium.py run wav rust nwav controls/wav/four-samples.wav
```
