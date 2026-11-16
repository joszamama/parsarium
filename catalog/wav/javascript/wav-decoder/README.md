# wav-decoder — WAV / JavaScript

- **Pinned release:** `1.3.0`
- **License:** MIT
- **Parsed scope:** samples
- **Underlying family:** wav-decoder
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wav-decoder>)
- **Catalog evidence:** [parser record](../../../../data/javascript/wav/parsers.json) · [control verification](../../../../data/javascript/wav/verification.json) · [within-ecosystem ranking](../../../../data/javascript/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "sampleCount": 4,
  "sampleSigns": [
    0,
    1,
    -1,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
