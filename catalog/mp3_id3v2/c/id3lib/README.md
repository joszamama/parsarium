# id3lib — MP3 with ID3v2 / C

- **Pinned release:** `3.8.3`
- **License:** LGPL-2.0-or-later
- **Parsed scope:** ID3v2 title and frame count in a valid tagged MP3
- **Underlying family:** id3lib ID3v2 parser
- **Local input API:** `ID3Tag_LinkWithFlags(local filename, ID3TT_ID3V2); ID3Tag_FindFrameWithID(TIT2); ID3Field_GetASCII`
- **Documentation:** [API reference](<https://id3lib.sourceforge.net/api/index.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "frames": 4
}
```

The C API wraps the same C++ id3lib engine used by the native C++ adapter. Both are one package path per ecosystem, not independent tag parsers.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/id3lib/README.md)

```sh
python3 parsarium.py build mp3_id3v2 c id3lib
python3 parsarium.py run mp3_id3v2 c id3lib controls/mp3_id3v2/tone-tags.mp3
```
