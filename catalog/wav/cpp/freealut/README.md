# freealut — WAV / C++

- **Pinned release:** `1.1.0`
- **License:** LGPL-2.0-only
- **Parsed scope:** WAV format, sample rate, frame count and four decoded PCM samples
- **Underlying family:** FreeALUT WAV memory loader
- **Local input API:** `alutInit; alutLoadMemoryFromFile(local WAV path, format, size, frequency); alutExit`
- **Documentation:** [API reference](<https://github.com/vancegroup/freealut/blob/freealut_1_1_0/include/AL/alut.h>)
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

Own tagged C WAV loader package; this API requires an OpenAL context, created by alutInit on macOS. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
