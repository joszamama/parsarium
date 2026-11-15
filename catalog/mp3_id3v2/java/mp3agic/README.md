# mp3agic — MP3 with ID3v2 / Java

- **Pinned release:** `0.9.1`
- **License:** MIT
- **Parsed scope:** local MP3 frames and ID3v2 title, artist, album and API tag version
- **Underlying family:** mp3agic native MP3 frame and ID3v2 reader
- **Local input API:** `new Mp3File(Path), hasId3v2Tag(), getId3v2Tag()`
- **Documentation:** [API reference](<https://github.com/mpatric/mp3agic/blob/master/readme.md>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "tag_version": "3.0"
}
```

jid3lib's project README identifies mp3agic as a fork in the same historical lineage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
