# jaffree — WAV / Java

- **Pinned release:** `2024.08.29`
- **License:** Apache-2.0
- **Parsed scope:** PCM codec, sample rate and channels
- **Underlying family:** Jaffree wrapper over local FFprobe/FFmpeg
- **Local input API:** `FFprobe.atPath(Path localExecutableDir).setShowStreams(true).setInput(Path localWav).execute().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "codec": "pcm_s16le",
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
