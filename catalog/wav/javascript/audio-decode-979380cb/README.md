# @audio/decode — WAV / JavaScript

- **Pinned release:** `4.3.0`
- **License:** MIT
- **Parsed scope:** samples
- **Underlying family:** audiojs/decode
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode>)
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
