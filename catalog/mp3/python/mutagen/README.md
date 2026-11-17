# mutagen — MP3 / Python

- **Pinned release:** `1.48.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** Mutagen MP3/ID3 parser
- **Local input API:** `mutagen.mp3.MP3(local path)`
- **Documentation:** [API reference](<https://mutagen.readthedocs.io/en/latest/api/wave.html>)
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

[Docker harness and verification receipt](../../../../projects/mp3/python/mutagen/README.md)

```sh
python3 parsarium.py build mp3 python mutagen
python3 parsarium.py run mp3 python mutagen controls/mp3/id3v2-tagged-tone.mp3
```
