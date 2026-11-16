# wavefile-reader — WAV / JavaScript

- **Pinned release:** `1.1.1`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** rochars/wavefile
- **Local input API:** `new WaveFileReader(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wavefile-reader>)
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

[Docker harness and verification receipt](../../../../projects/wav/javascript/wavefile_reader/README.md)

```sh
python3 parsarium.py build wav javascript wavefile_reader
python3 parsarium.py run wav javascript wavefile_reader controls/wav/four-samples.wav
```
