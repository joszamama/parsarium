# audiostreamify/hvap — MP3 with ID3v2 / PHP

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `Processor::audio(local tagged MP3 path)->analyze(); ID3v2 title/artist/album and major version`
- **Documentation:** [API reference](<https://github.com/audiostreamify/hvap/blob/e9c0c63e9d7ed13f03b152c01452008b2076fc96/src/Mocks/ID3Tags.php>)
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

The documented Audio constructor accepts a file path and the ID3Tags trait documents analyze(); the pinned package delegates to james-heinrich/getid3 v1.9.28. Other HVAP features require Linux tools, but this read API passed on macOS.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/audiostreamify_hvap/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php audiostreamify_hvap
python3 parsarium.py run mp3_id3v2 php audiostreamify_hvap controls/mp3_id3v2/tone-tags.mp3
```
