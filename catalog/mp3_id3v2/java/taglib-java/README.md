# taglib-java — MP3 with ID3v2 / Java

- **Pinned release:** `1.0.0`
- **License:** LGPL-2.1 OR MPL-2.0
- **Parsed scope:** local tagged MP3 title, artist, album and sample rate
- **Underlying family:** TagLib Java adaptation with native Java MPEG and ID3v2 implementation
- **Local input API:** `new MpegFile(Path).hasId3v2Tag(), id3v2Tag(), detailedProperties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/cz/skyba/taglib/1.0.0/taglib-1.0.0-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "frequency": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/taglib_java/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java taglib_java
python3 parsarium.py run mp3_id3v2 java taglib_java controls/mp3_id3v2/tone-tags.mp3
```
