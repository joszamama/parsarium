# sempia/getid3 — MP3 with ID3v2 / PHP

- **Pinned release:** `2.0.0.0-p1.9.25`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `JamesHeinrich\GetID3\GetID3::analyze(local tagged MP3 path); tags.id3v2 title/artist/album and ID3v2 major version`
- **Documentation:** [API reference](<https://gitlab.com/Sempia/getID3/-/blob/46405ae39a503ac72d1ce5b31f6f11f938f034ed/README.md>)
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

Namespaced PSR-4 fork periodically merged from upstream getID3; distinct Composer release path, same underlying getID3 parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
