# dgoriaev/mp3info — MP3 with ID3v2 / PHP

- **Pinned release:** `1.0.3`
- **License:** LGPL-3.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** Mp3Info native MP3 and ID3v2 parser
- **Local input API:** `dgoriaev\Mp3Info\Mp3Info(local tagged MP3 path, parseTags=true); tags2 TIT2/TPE1/TALB and ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/DplusG/Mp3Info/blob/64e790cd31d35d8ae3d5e3d8120f69aabd5ce0de/README.md>)
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

Fork of wapmorgan/Mp3Info with a changed namespace; distinct Composer package path, shared Mp3Info parser lineage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
