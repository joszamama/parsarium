# kiwilan/php-audio — MP3 with ID3v2 / PHP

- **Pinned release:** `4.0.02`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, and album
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `Audio::read(local tagged MP3 path); getTitle/getArtist/getAlbum`
- **Documentation:** [API reference](<https://github.com/kiwilan/php-audio/blob/684002b34e5db3fa2935d6b9ba8cba0ebd81b1a7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Audio delegates to james-heinrich/getid3 v1.9.22 in its isolated lock; this is a distinct wrapper package path but shares the getID3 parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
