# tika-audiovideo — MP3 with ID3v2 / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** local tagged MP3 title, artist and album metadata
- **Underlying family:** Apache Tika native MP3 and ID3v2 parser
- **Local input API:** `Mp3Parser.parse(TikaInputStream, ContentHandler, Metadata, ParseContext)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-sources.jar>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/tika_audiovideo/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java tika_audiovideo
python3 parsarium.py run mp3_id3v2 java tika_audiovideo controls/mp3_id3v2/tone-tags.mp3
```
