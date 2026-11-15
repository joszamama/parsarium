# owen-oj/laravel-getid3 — MP3 with ID3v2 / PHP

- **Pinned release:** `v2.6.0`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `GetId3(local tagged MP3 path); getTitle/getArtist/getAlbum and extractInfo ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/Owen-oj/laravel-getid3/blob/6b89fc96b3dd2536fb2e53f8fee99ee6b76f9fd1/readme.md>)
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

Laravel wrapper delegates to the same pinned james-heinrich/getid3 package in this lock; a separate package path, not an independent parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
