# wavefile — WAV / JavaScript

- **Pinned release:** `11.0.0`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** rochars/wavefile
- **Local input API:** `new WaveFile(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wavefile>)
- **Catalog evidence:** [parser record](../../../../data/javascript/wav/parsers.json) · [control verification](../../../../data/javascript/wav/verification.json) · [within-ecosystem ranking](../../../../data/javascript/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "bitsPerSample": 16
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
