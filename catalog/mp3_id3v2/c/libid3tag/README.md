# libid3tag — MP3 with ID3v2 / C

- **Pinned release:** `0.16.4`
- **License:** GPL-2.0-or-later
- **Parsed scope:** ID3v2 title and normalized tag version/frame count
- **Underlying family:** libid3tag ID3v2 metadata parser
- **Local input API:** `id3_file_open(local filename); id3_file_tag; id3_tag_findframe(TIT2); id3_field_getstrings`
- **Documentation:** [API reference](<https://codeberg.org/tenacityteam/libid3tag/src/tag/0.16.4/include/id3tag.h.in>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "normalized_id3_major": 4,
  "frames": 4
}
```

The same C ID3v2 parser serves C and C++ call sites. Its API normalizes the input 2.3 tag to internal major version 4; it does not decode MPEG audio frames.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/libid3tag/README.md)

```sh
python3 parsarium.py build mp3_id3v2 c libid3tag
python3 parsarium.py run mp3_id3v2 c libid3tag controls/mp3_id3v2/tone-tags.mp3
```
