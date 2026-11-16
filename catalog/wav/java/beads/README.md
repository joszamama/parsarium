# beads — WAV / Java

- **Pinned release:** `3.2`
- **License:** GPL-3.0-only
- **Parsed scope:** sample rate, channels and decoded frame count
- **Underlying family:** Beads WAV reader
- **Local input API:** `new WavFileReaderWriter().readAudioFile(String localPath), getSampleAudioFormat()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/beadsproject/beads/3.2/beads-3.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 256
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/beads/README.md)

```sh
python3 parsarium.py build wav java beads
python3 parsarium.py run wav java beads controls/wav/256-samples.wav
```
