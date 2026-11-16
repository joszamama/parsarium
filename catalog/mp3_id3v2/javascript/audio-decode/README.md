# @audio/decode — MP3 with ID3v2 / JavaScript

- **Pinned release:** `4.3.0`
- **License:** MIT
- **Parsed scope:** decoded_audio
- **Underlying family:** mpg123 WASM
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "samples": 8000
}
```

Facade delegates MP3 decoding to @audio/decode-mp3 and mpg123-decoder WASM.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
