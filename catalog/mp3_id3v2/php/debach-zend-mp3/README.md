# debach/zend-mp3 — MP3 with ID3v2 / PHP

- **Pinned release:** `1.8.1`
- **License:** BSD-3-Clause
- **Parsed scope:** ID3v2.3 title, artist, and album
- **Underlying family:** Sven Vollbehr PHP Reader ID3 family
- **Local input API:** `Zend_Media_Id3v2(local tagged MP3 path); getFramesByIdentifier(TIT2/TPE1/TALB) and frame getText()`
- **Documentation:** [API reference](<https://github.com/debach/zend-mp3/blob/17b523ad57f283ddf3a116bc0eff22cb9d1b4b27/README.md>)
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

Composer fork of Sven Vollbehr PHP Reader; its ID3 parser shares source lineage with vollbehr/php-reader. A distinct package path, not an independent parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/debach_zend_mp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php debach_zend_mp3
python3 parsarium.py run mp3_id3v2 php debach_zend_mp3 controls/mp3_id3v2/tone-tags.mp3
```
