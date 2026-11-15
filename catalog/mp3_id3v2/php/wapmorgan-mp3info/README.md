# wapmorgan/mp3info — MP3 with ID3v2 / PHP

- **Pinned release:** `0.1.1`
- **License:** LGPL-3.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** Mp3Info native MP3 and ID3v2 parser
- **Local input API:** `Mp3Info(local tagged MP3 path, parseTags=true); tags2 TIT2/TPE1/TALB and ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/wapmorgan/Mp3Info/blob/e532c2e1997874f9c672c7810ce90ef15004ef94/README.md>)
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

Own ID3v2.3 and MPEG audio parser; the pinned release README states that ID3v2.2 and v2.4 are unsupported.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
