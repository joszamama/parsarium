# jid3lib — MP3 with ID3v2 / Java

- **Pinned release:** `0.5.4`
- **License:** LGPL-2.1
- **Parsed scope:** local tagged MP3 title, artist and album
- **Underlying family:** jid3lib native ID3v2 tag parser; historical ancestry shared with jaudiotagger and mp3agic
- **Local input API:** `new MP3File(File).getID3v2Tag(), getSongTitle(), getLeadArtist(), getAlbumTitle()`
- **Documentation:** [API reference](<https://github.com/ericfarng/jid3lib>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
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
