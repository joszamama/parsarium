# mhor/php-mediainfo — MP3 / PHP

- **Pinned release:** `5.8.0`
- **Upstream:** [source repository](<https://github.com/mhor/php-mediainfo>) · [Packagist](<https://packagist.org/packages/mhor/php-mediainfo>)
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, performer, and album on an 18-second MP3
- **Underlying family:** MediaInfoLib native MP3 and ID3 parser
- **Local input API:** `MediaInfo::getInfo(local tagged MP3 path); getGeneral() title/performer/album`
- **Documentation:** [API reference](<https://github.com/mhor/php-mediainfo/blob/a0be4ef4dc1f56292793ad31c2b3efc75bfdbf05/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-long.mp3`](../../../../controls/mp3/id3v2-tagged-tone-long.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Composer wrapper invokes the external MediaInfo 26.10 CLI; this is a package path over the MediaInfoLib parser family. The longer valid control is needed for the backend to read sufficient audio bytes.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/php/mhor_php_mediainfo/README.md)

```sh
python3 parsarium.py build mp3 php mhor_php_mediainfo
python3 parsarium.py run mp3 php mhor_php_mediainfo controls/mp3/id3v2-tagged-tone-long.mp3
```
