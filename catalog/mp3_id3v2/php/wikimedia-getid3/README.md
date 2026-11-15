# wikimedia/getid3 — MP3 with ID3v2 / PHP

- **Pinned release:** `v2.0.0-beta5`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `JamesHeinrich\GetID3\GetID3::analyze(local tagged MP3 path); ID3v2 title/artist/album and major version`
- **Documentation:** [API reference](<https://github.com/wikimedia/getID3/blob/4e7aca96e7f4cf5ce6e08bca998334f567259965/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
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

Wikimedia fork of the upstream namespaced getID3 beta; distinct Composer package path, shared getID3 parser lineage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
