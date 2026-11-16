# mutagen — MP3 with ID3v2 / Python

- **Pinned release:** `1.48.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** Mutagen MP3/ID3 parser
- **Local input API:** `mutagen.mp3.MP3(local path)`
- **Documentation:** [API reference](<https://mutagen.readthedocs.io/en/latest/api/wave.html>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
