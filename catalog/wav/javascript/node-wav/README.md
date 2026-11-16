# node-wav — WAV / JavaScript

- **Pinned release:** `0.0.2`
- **License:** MIT
- **Parsed scope:** samples
- **Underlying family:** node-wav
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-wav>)
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

[Docker harness and verification receipt](../../../../projects/wav/javascript/node_wav/README.md)

```sh
python3 parsarium.py build wav javascript node_wav
python3 parsarium.py run wav javascript node_wav controls/wav/four-samples.wav
```
