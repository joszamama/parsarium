# music-metadata — WAV / JavaScript

- **Pinned release:** `12.4.0`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** music-metadata
- **Local input API:** `parseBuffer(Buffer, {mimeType:"audio/wav"})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/music-metadata>)
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
