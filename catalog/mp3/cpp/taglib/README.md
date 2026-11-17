# taglib — MP3 / C++

- **Pinned release:** `2.3.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** ID3v2 title and artist from a valid tagged MP3
- **Underlying family:** TagLib ID3v2 parser
- **Local input API:** `TagLib::MPEG::File(local filename); ID3v2Tag()->title()/artist()`
- **Documentation:** [API reference](<https://taglib.org/api/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3/parsers.json) · [control verification](../../../../data/cpp/mp3/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control"
}
```

The C simple API delegates to the TagLib C++ core; C and C++ share the same ID3v2 engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/cpp/taglib/README.md)

```sh
python3 parsarium.py build mp3 cpp taglib
python3 parsarium.py run mp3 cpp taglib controls/mp3/id3v2-tagged-tone.mp3
```
