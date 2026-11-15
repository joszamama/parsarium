# jdsp — WAV / Java

- **Pinned release:** `3.1.1`
- **License:** MIT
- **Parsed scope:** sample rate, channels and frame count
- **Underlying family:** JDSP WAV API over wavfile
- **Local input API:** `new WAV().readWAV(String localPath), getProperties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/psambit9791/jdsp/3.1.1/jdsp-3.1.1-javadoc.jar>)
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
