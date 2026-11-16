# audiotags — MP3 with ID3v2 / Rust

- **Pinned release:** `0.5.0`
- **License:** MIT
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** audiotags via id3
- **Local input API:** `Tag::new().read_from_path(path)`
- **Documentation:** [API reference](<https://docs.rs/audiotags/0.5.0/audiotags/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/audiotags/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust audiotags
python3 parsarium.py run mp3_id3v2 rust audiotags controls/mp3_id3v2/tone-tags.mp3
```
