# mp3agic — MP3 / Java

- **Pinned release:** `0.9.1`
- **Upstream:** [source repository](<https://github.com/mpatric/mp3agic>) · [Maven Central](<https://central.sonatype.com/artifact/com.mpatric/mp3agic>)
- **License:** MIT
- **Parsed scope:** local MP3 frames and ID3v2 title, artist, album and API tag version
- **Underlying family:** mp3agic native MP3 frame and ID3v2 reader
- **Local input API:** `new Mp3File(Path), hasId3v2Tag(), getId3v2Tag()`
- **Documentation:** [API reference](<https://github.com/mpatric/mp3agic/blob/master/readme.md>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/mp3agic/README.md)

```sh
python3 parsarium.py build mp3 java mp3agic
python3 parsarium.py run mp3 java mp3agic controls/mp3/id3v2-tagged-tone.mp3
```
