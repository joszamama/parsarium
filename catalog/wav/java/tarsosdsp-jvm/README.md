# tarsosdsp-jvm — WAV / Java

- **Pinned release:** `2.5`
- **License:** GPL-3.0-only
- **Parsed scope:** sample rate, channels, bit depth and decoded frame count
- **Underlying family:** TarsosDSP JVM wrapper over Java Sound
- **Local input API:** `AudioDispatcherFactory.fromFile(File,int,int), AudioDispatcher.getFormat() and run()`
- **Documentation:** [API reference](<https://mvn.0110.be/releases/be/tarsos/dsp/jvm/2.5/jvm-2.5-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16,
  "frames": 256
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
