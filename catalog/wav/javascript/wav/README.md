# wav — WAV / JavaScript

- **Pinned release:** `1.0.2`
- **Upstream:** [source repository](<https://github.com/TooTallNate/node-wav>) · [npm](<https://www.npmjs.com/package/wav>)
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** node-wav-stream
- **Local input API:** `new Reader(); Readable.from([Buffer]).pipe(reader)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wav>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/javascript/wav/README.md)

```sh
python3 parsarium.py build wav javascript wav
python3 parsarium.py run wav javascript wav controls/wav/four-samples.wav
```
