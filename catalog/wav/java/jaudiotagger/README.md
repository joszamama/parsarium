# jaudiotagger — WAV / Java

- **Pinned release:** `3.0.1`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** WAV header sample rate, channels and bit depth
- **Underlying family:** jaudiotagger WAV reader
- **Local input API:** `AudioFileIO.read(File).getAudioHeader()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": "1",
  "bits": 16
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/jaudiotagger/README.md)

```sh
python3 parsarium.py build wav java jaudiotagger
python3 parsarium.py run wav java jaudiotagger controls/wav/256-samples.wav
```
