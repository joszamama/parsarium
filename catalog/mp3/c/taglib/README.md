# taglib — MP3 / C

- **Pinned release:** `2.3.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** ID3v2 title and artist from a valid tagged MP3
- **Underlying family:** TagLib ID3v2 parser
- **Local input API:** `taglib_file_new_type(local filename, TagLib_File_MPEG); taglib_tag_title/artist`
- **Documentation:** [API reference](<https://taglib.org/api/>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control"
}
```

The C simple API delegates to the TagLib C++ core; C and C++ share the same ID3v2 engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/taglib/README.md)

```sh
python3 parsarium.py build mp3 c taglib
python3 parsarium.py run mp3 c taglib controls/mp3_id3v2/tone-tags.mp3
```
