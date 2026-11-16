# music-tag — MP3 with ID3v2 / Python

- **Pinned release:** `0.4.3`
- **License:** MIT
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** music-tag via Mutagen
- **Local input API:** `music_tag.load_file(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/music-tag/0.4.3/>)
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
