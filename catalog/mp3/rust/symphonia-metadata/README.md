# symphonia-metadata — MP3 / Rust

- **Pinned release:** `0.6.1`
- **Upstream:** [source repository](<https://github.com/pdeljanov/Symphonia>) · [crates.io](<https://crates.io/crates/symphonia-metadata>)
- **License:** MPL-2.0
- **Parsed scope:** ID3v2 frame keys
- **Underlying family:** Symphonia ID3v2 reader
- **Local input API:** `Id3v2Reader::try_new(MediaSourceStream).read_all()`
- **Documentation:** [API reference](<https://docs.rs/symphonia-metadata/0.6.1/symphonia_metadata/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control verification](../../../../data/rust/mp3/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "tag_count": 4,
  "keys": [
    "TIT2",
    "TPE1",
    "TALB",
    "TSSE"
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/rust/symphonia_metadata/README.md)

```sh
python3 parsarium.py build mp3 rust symphonia_metadata
python3 parsarium.py run mp3 rust symphonia_metadata controls/mp3/id3v2-tagged-tone.mp3
```
