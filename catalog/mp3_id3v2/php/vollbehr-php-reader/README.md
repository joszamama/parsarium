# vollbehr/php-reader — MP3 with ID3v2 / PHP

- **Pinned release:** `v2.0-rc1`
- **License:** BSD-3-Clause
- **Parsed scope:** ID3v2.3 title, artist, and album
- **Underlying family:** Sven Vollbehr PHP Reader ID3 family
- **Local input API:** `FileReader(local tagged MP3 path) passed to Vollbehr\Media\Id3v2; getFramesByIdentifier(TIT2/TPE1/TALB) and frame getText()`
- **Documentation:** [API reference](<https://github.com/vollbehr/php-reader/blob/e1147f8b471d937077ed7bbbba31a87586ad24a5/README.md>)
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

Modern framework-agnostic PHP Reader release; same original author and code lineage as debach/zend-mp3, but distinct Composer package path.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/vollbehr_php_reader/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php vollbehr_php_reader
python3 parsarium.py run mp3_id3v2 php vollbehr_php_reader controls/mp3_id3v2/tone-tags.mp3
```
