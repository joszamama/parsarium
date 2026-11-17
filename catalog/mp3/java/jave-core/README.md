# jave-core — MP3 / Java

- **Pinned release:** `4.2.0`
- **License:** GPL-3.0-only
- **Parsed scope:** local tagged MP3 format, codec, sample rate and channels
- **Underlying family:** JAVE2 wrapper over bundled FFmpeg MP3 demuxer
- **Local input API:** `new MultimediaObject(File).getInfo().getAudio()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3 (mp3float)",
  "frequency": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/jave_core/README.md)

```sh
python3 parsarium.py build mp3 java jave_core
python3 parsarium.py run mp3 java jave_core controls/mp3/id3v2-tagged-tone.mp3
```
