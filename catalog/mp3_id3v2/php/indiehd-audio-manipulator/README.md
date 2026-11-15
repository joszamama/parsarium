# indiehd/audio-manipulator — MP3 with ID3v2 / PHP

- **Pinned release:** `v4.1.0`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `IndieHD\AudioManipulator\MediaParsing\MediaParser::analyze(local tagged MP3 path); tags.id3v2 title/artist/album and ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/indiehd/audio-manipulator/blob/1e2f6d76030200c77cd727b40d3ea6166957f45d/src/MediaParsing/MediaParserInterface.php>)
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

Public MediaParserInterface specifies analyze(string $file), and implementation delegates to pinned james-heinrich/getid3 v1.9.23. Separate package path, same underlying getID3 parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
