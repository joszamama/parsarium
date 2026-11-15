# wav-file-info — WAV / JavaScript

- **Pinned release:** `0.0.10`
- **License:** ISC
- **Parsed scope:** header
- **Underlying family:** wav-file-info
- **Local input API:** `infoByFilename(path, callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wav-file-info>)
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
