# raylib — WAV / C++

- **Pinned release:** `6.2`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** raylib bundled dr_wav decoder
- **Local input API:** `LoadWave(local WAV path); Wave.sampleRate, channels, frameCount, data; UnloadWave`
- **Documentation:** [API reference](<https://github.com/raysan5/raylib/blob/6.2/src/raylib.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

Distinct raylib package C loading API; WAV implementation shares dr_wav family. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
