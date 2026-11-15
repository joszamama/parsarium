# AudioSystem.getAudioFileFormat(File) — WAV / Java

- **Runtime:** OpenJDK 25, Java SE 25 API inventory
- **Input API:** `AudioSystem.getAudioFileFormat(File)`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/25/docs/api/java.desktop/javax/sound/sampled/AudioSystem.html)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../../controls/wav/256-samples.wav)
- **Inventory and verification:** [standard API record](../../../../../data/java/wav/standard.json) · [saved result](../../../../../data/java/wav/verification.json)

**Parser family:** OpenJDK Java Sound WAVE file reader

## Observed control result

```json
{
  "type": "WAVE",
  "sample_rate": 8000,
  "channels": 1,
  "frames": 256
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
