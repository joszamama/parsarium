# AudioSystem.getAudioInputStream(File) — WAV / Java

- **Runtime:** Eclipse Temurin OpenJDK 21.0.2 linux/arm64 java.desktop
- **Input API:** `AudioSystem.getAudioInputStream(File)`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/sound/sampled/AudioSystem.html)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../../controls/wav/256-samples.wav)
- **Inventory and verification:** [standard API record](../../../../../data/java/wav/standard.json) · [saved result](../../../../../data/java/wav/verification.json)

**Parser family:** OpenJDK Java Sound WAVE file reader

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 256,
  "sample_bytes": 8
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
