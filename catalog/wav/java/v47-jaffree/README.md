# v47-jaffree — WAV / Java

- **Pinned release:** `2.1.0`
- **License:** GPL-3.0-only
- **Parsed scope:** PCM codec, sample rate and channels
- **Underlying family:** v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg
- **Local input API:** `FFprobe.atPath(Path localBin).setShowStreams(true).setInput(Path localWav).execute()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar>)
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
