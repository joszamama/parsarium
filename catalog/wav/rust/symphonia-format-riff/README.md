# symphonia-format-riff — WAV / Rust

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parsed scope:** WAV track metadata and audio packet
- **Underlying family:** Symphonia WAV demuxer
- **Local input API:** `WavReader::try_new(MediaSourceStream, FormatOptions).next_packet()`
- **Documentation:** [API reference](<https://docs.rs/symphonia-format-riff/0.6.1/symphonia_format_riff/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/symphonia_format_riff/README.md)

```sh
python3 parsarium.py build wav rust symphonia_format_riff
python3 parsarium.py run wav rust symphonia_format_riff controls/wav/four-samples.wav
```
