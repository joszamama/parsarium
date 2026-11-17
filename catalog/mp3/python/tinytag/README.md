# tinytag — MP3 / Python

- **Pinned release:** `2.3.2`
- **License:** MIT
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** TinyTag MP3/ID3 parser
- **Local input API:** `tinytag.TinyTag.get(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/tinytag/2.3.2/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control verification](../../../../data/python/mp3/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/python/tinytag/README.md)

```sh
python3 parsarium.py build mp3 python tinytag
python3 parsarium.py run mp3 python tinytag controls/mp3/id3v2-tagged-tone.mp3
```
