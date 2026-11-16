# prx-wavefile — WAV / JavaScript

- **Pinned release:** `11.0.0-prx.6`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** rochars/wavefile
- **Local input API:** `new WaveFile(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/prx-wavefile>)
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

Published variant of the wavefile parser; shared family records common origin, not independent implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/javascript/prx_wavefile/README.md)

```sh
python3 parsarium.py build wav javascript prx_wavefile
python3 parsarium.py run wav javascript prx_wavefile controls/wav/four-samples.wav
```
