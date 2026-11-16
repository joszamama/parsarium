# lofty — MP3 with ID3v2 / Rust

- **Pinned release:** `0.25.5`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** Lofty MPEG/ID3 parser
- **Local input API:** `read_from_path(path).primary_tag().title()/artist()/album()`
- **Documentation:** [API reference](<https://docs.rs/lofty/0.25.5/lofty/>)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/lofty/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust lofty
python3 parsarium.py run mp3_id3v2 rust lofty controls/mp3_id3v2/tone-tags.mp3
```
