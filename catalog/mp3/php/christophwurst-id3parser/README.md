# christophwurst/id3parser — MP3 / PHP

- **Pinned release:** `v0.1.4`
- **License:** GPL-3.0-or-later
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3-derived ID3 tag parser
- **Local input API:** `ID3Parser::analyze(local tagged MP3 path); ID3v2 comments title/artist/album and major version`
- **Documentation:** [API reference](<https://github.com/ChristophWurst/ID3Parser/blob/050c9d81ea89b0cf53e23a27efc4e1840f9ab260/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "id3v2_major": 3
}
```

This package vendors a stripped-down getID3 ID3 implementation; it is a separate package path, not an independent parser family. Packagist marks it abandoned in favor of nextcloud/id3parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/christophwurst_id3parser/README.md)

```sh
python3 parsarium.py build mp3 php christophwurst_id3parser
python3 parsarium.py run mp3 php christophwurst_id3parser controls/mp3_id3v2/tone-tags.mp3
```
