# jave-core — WAV / Java

- **Pinned release:** `4.2.0`
- **License:** GPL-3.0-only
- **Parsed scope:** WAV format, PCM codec, sample rate and channels
- **Underlying family:** JAVE2 wrapper over bundled FFmpeg
- **Local input API:** `new MultimediaObject(File localWav).getInfo().getAudio()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "codec": "pcm_s16le ([1][0][0][0] / 0x0001)",
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
