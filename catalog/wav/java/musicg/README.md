# musicg — WAV / Java

- **Pinned release:** `1.4.2.2`
- **License:** Apache-2.0
- **Parsed scope:** WAVE format, sample rate, channels, bit depth and sample count
- **Underlying family:** musicg PCM WAVE reader
- **Local input API:** `new Wave(String localPath).getWaveHeader(), getSampleAmplitudes()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/fracpete/musicg/1.4.2.2/musicg-1.4.2.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "WAVE",
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16,
  "samples": 256
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
