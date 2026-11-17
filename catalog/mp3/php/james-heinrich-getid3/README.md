# james-heinrich/getid3 — MP3 / PHP

- **Pinned release:** `v1.9.28`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `getID3::analyze(local tagged MP3 path); ID3v2 title/artist/album and major version`
- **Documentation:** [API reference](<https://github.com/JamesHeinrich/getID3/blob/be83ea6ffbdac0301d83bee0d42f09e2a41bd0dd/README.md>)
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

Multi-format getID3 package; this adapter uses its own ID3v2 and MPEG audio parsers.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/getid3/README.md)

```sh
python3 parsarium.py build mp3 php getid3
python3 parsarium.py run mp3 php getid3 controls/mp3_id3v2/tone-tags.mp3
```
