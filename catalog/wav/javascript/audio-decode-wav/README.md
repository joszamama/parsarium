# @audio/decode-wav — WAV / JavaScript

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** samples
- **Underlying family:** audiojs/decode
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode-wav>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/javascript/audio_decode_wav/README.md)

```sh
python3 parsarium.py build wav javascript audio_decode_wav
python3 parsarium.py run wav javascript audio_decode_wav controls/wav/four-samples.wav
```
