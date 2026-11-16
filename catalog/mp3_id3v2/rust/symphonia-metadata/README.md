# symphonia-metadata — MP3 with ID3v2 / Rust

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parsed scope:** ID3v2 frame keys
- **Underlying family:** Symphonia ID3v2 reader
- **Local input API:** `Id3v2Reader::try_new(MediaSourceStream).read_all()`
- **Documentation:** [API reference](<https://docs.rs/symphonia-metadata/0.6.1/symphonia_metadata/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/symphonia_metadata/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust symphonia_metadata
python3 parsarium.py run mp3_id3v2 rust symphonia_metadata controls/mp3_id3v2/tone-tags.mp3
```
