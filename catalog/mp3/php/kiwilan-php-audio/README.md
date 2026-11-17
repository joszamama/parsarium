# kiwilan/php-audio — MP3 / PHP

- **Pinned release:** `4.0.02`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, and album
- **Underlying family:** getID3 native MP3 and ID3v2 parser
- **Local input API:** `Audio::read(local tagged MP3 path); getTitle/getArtist/getAlbum`
- **Documentation:** [API reference](<https://github.com/kiwilan/php-audio/blob/684002b34e5db3fa2935d6b9ba8cba0ebd81b1a7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Audio delegates to james-heinrich/getid3 v1.9.22 in its isolated lock; this is a distinct wrapper package path but shares the getID3 parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/php/kiwilan_php_audio/README.md)

```sh
python3 parsarium.py build mp3 php kiwilan_php_audio
python3 parsarium.py run mp3 php kiwilan_php_audio controls/mp3/id3v2-tagged-tone.mp3
```
