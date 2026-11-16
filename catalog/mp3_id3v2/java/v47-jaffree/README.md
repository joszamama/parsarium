# v47-jaffree — MP3 with ID3v2 / Java

- **Pinned release:** `2.1.0`
- **License:** GPL-3.0-only
- **Parsed scope:** local tagged MP3 codec, sample rate, channels and title
- **Underlying family:** v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg
- **Local input API:** `FFprobe.atPath(Path localBin).setShowStreams(true).setShowFormat(true).setInput(Path localMp3).execute()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "codec": "mp3",
  "frequency": 8000,
  "channels": 1,
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/v47_jaffree/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java v47_jaffree
python3 parsarium.py run mp3_id3v2 java v47_jaffree controls/mp3_id3v2/tone-tags.mp3
```
