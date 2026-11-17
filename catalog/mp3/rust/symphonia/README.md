# symphonia — MP3 / Rust

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parsed scope:** MP3 track header and audio packet
- **Underlying family:** Symphonia MP3 demuxer
- **Local input API:** `default::get_probe().probe(Hint, MediaSourceStream).next_packet()`
- **Documentation:** [API reference](<https://docs.rs/symphonia/0.6.1/symphonia/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control verification](../../../../data/rust/mp3/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "packet_bytes": 288
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/rust/symphonia/README.md)

```sh
python3 parsarium.py build mp3 rust symphonia
python3 parsarium.py run mp3 rust symphonia controls/mp3/id3v2-tagged-tone.mp3
```
