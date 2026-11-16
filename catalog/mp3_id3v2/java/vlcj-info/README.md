# vlcj-info — MP3 with ID3v2 / Java

- **Pinned release:** `2.0.3`
- **License:** GPL-3.0-or-later
- **Parsed scope:** local tagged MP3 format, sample rate, channels and title
- **Underlying family:** vlcj-info JNA binding to libmediainfo
- **Local input API:** `new MediaInfoFile(String localMp3).open(), info(String MediaInfo template)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/uk/co/caprica/vlcj-info/2.0.3/vlcj-info-2.0.3-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "format": "MPEG Audio",
  "frequency": 8000,
  "channels": 1,
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/vlcj_info/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java vlcj_info
python3 parsarium.py run mp3_id3v2 java vlcj_info controls/mp3_id3v2/tone-tags.mp3
```
