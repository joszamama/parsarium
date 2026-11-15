# id3 — MP3 with ID3v2 / Rust

- **Pinned release:** `1.17.3`
- **License:** MIT
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** id3 tag parser
- **Local input API:** `Tag::read_from_path(path).title()/artist()/album()`
- **Documentation:** [API reference](<https://docs.rs/id3/1.17.3/id3/>)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/id3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust id3
python3 parsarium.py run mp3_id3v2 rust id3 controls/mp3_id3v2/tone-tags.mp3
```
