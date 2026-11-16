# oxideav-id3 — MP3 with ID3v2 / Rust

- **Pinned release:** `0.0.7`
- **License:** MIT
- **Parsed scope:** ID3v2 version, frame count, consumed bytes
- **Underlying family:** oxideav ID3 reader
- **Local input API:** `parse_tag(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/oxideav-id3/0.0.7/oxideav_id3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "version": "V2_3",
  "frame_count": 4,
  "tag_bytes": 101
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/oxideav_id3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust oxideav_id3
python3 parsarium.py run mp3_id3v2 rust oxideav_id3 controls/mp3_id3v2/tone-tags.mp3
```
