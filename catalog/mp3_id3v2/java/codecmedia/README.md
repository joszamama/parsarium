# codecmedia — MP3 with ID3v2 / Java

- **Pinned release:** `1.2.2`
- **License:** Apache-2.0
- **Parsed scope:** local tagged MP3 codec, sample rate and channels
- **Underlying family:** CodecMedia native MP3 frame parser
- **Local input API:** `CodecMedia.createDefault().probe(Path).streams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "codec": "mp3",
  "frequency": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/codecmedia/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java codecmedia
python3 parsarium.py run mp3_id3v2 java codecmedia controls/mp3_id3v2/tone-tags.mp3
```
