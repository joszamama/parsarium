# wapmorgan/mp3info — MP3 / PHP

- **Pinned release:** `0.1.1`
- **Upstream:** [source repository](<https://github.com/wapmorgan/Mp3Info>) · [Packagist](<https://packagist.org/packages/wapmorgan/mp3info>)
- **License:** LGPL-3.0
- **Parsed scope:** ID3v2.3 title, artist, album, and major version
- **Underlying family:** Mp3Info native MP3 and ID3v2 parser
- **Local input API:** `Mp3Info(local tagged MP3 path, parseTags=true); tags2 TIT2/TPE1/TALB and ID3v2 major version`
- **Documentation:** [API reference](<https://github.com/wapmorgan/Mp3Info/blob/e532c2e1997874f9c672c7810ce90ef15004ef94/README.md>)
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

Own ID3v2.3 and MPEG audio parser; the pinned release README states that ID3v2.2 and v2.4 are unsupported.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/php/wapmorgan_mp3info/README.md)

```sh
python3 parsarium.py build mp3 php wapmorgan_mp3info
python3 parsarium.py run mp3 php wapmorgan_mp3info controls/mp3/id3v2-tagged-tone.mp3
```
