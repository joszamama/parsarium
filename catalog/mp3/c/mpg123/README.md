# mpg123 — MP3 / C

- **Pinned release:** `1.33.7`
- **License:** LGPL-2.1-only
- **Parsed scope:** ID3v2 title/version after scanning valid MP3 audio
- **Underlying family:** libmpg123 MPEG audio and ID3v2 parser
- **Local input API:** `mpg123_open(local filename); mpg123_scan; mpg123_id3(v2)->title`
- **Documentation:** [API reference](<https://www.mpg123.org/api/group__mpg123__metadata.shtml>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "id3v2_version": 3
}
```

The same C library is called from C and C++; mpg123_scan reads the audio stream and mpg123_id3 returns parsed ID3v2 fields.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/mpg123/README.md)

```sh
python3 parsarium.py build mp3 c mpg123
python3 parsarium.py run mp3 c mpg123 controls/mp3_id3v2/tone-tags.mp3
```
