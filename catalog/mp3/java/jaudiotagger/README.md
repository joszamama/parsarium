# jaudiotagger — MP3 / Java

- **Pinned release:** `3.0.1`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** local MP3 identification and ID3v2 title, artist and album
- **Underlying family:** jaudiotagger native MP3 and ID3v2 reader
- **Local input API:** `AudioFileIO.read(File), MP3File.getID3v2Tag(), Tag.getFirst(FieldKey)`
- **Documentation:** [API reference](<https://www.jthink.net/jaudiotagger/examples_id3.jsp>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

jid3lib's project README identifies jaudiotagger as a fork in the same historical lineage.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/jaudiotagger/README.md)

```sh
python3 parsarium.py build mp3 java jaudiotagger
python3 parsarium.py run mp3 java jaudiotagger controls/mp3_id3v2/tone-tags.mp3
```
