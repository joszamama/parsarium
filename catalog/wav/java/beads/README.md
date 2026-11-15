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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
