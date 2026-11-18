# indiehd/audio-manipulator — MP3 / PHP

- **Pinned release:** `v4.1.0`
- **Upstream:** [source repository](<https://github.com/indiehd/audio-manipulator>) · [Packagist](<https://packagist.org/packages/indiehd/audio-manipulator>)
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `IndieHD\AudioManipulator\MediaParsing\MediaParser::analyze(local tagged MP3 path); tags.id3v2 title/artist/album and ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/indiehd/audio-manipulator/blob/1e2f6d76030200c77cd727b40d3ea6166957f45d/src/MediaParsing/MediaParserInterface.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/php/indiehd_audio_manipulator/README.md)

```sh
python3 parsarium.py build mp3 php indiehd_audio_manipulator
python3 parsarium.py run mp3 php indiehd_audio_manipulator controls/mp3/id3v2-tagged-tone.mp3
```
