# node-bwf-wav-file-reader — WAV / JavaScript

- **Pinned release:** `1.0.4`
- **License:** ISC
- **Parsed scope:** header
- **Underlying family:** node-bwf-wav-file-reader
- **Local input API:** `readSync(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-bwf-wav-file-reader>)
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

[Docker harness and verification receipt](../../../../projects/wav/javascript/node_bwf_wav_file_reader/README.md)

```sh
python3 parsarium.py build wav javascript node_bwf_wav_file_reader
python3 parsarium.py run wav javascript node_bwf_wav_file_reader controls/wav/four-samples.wav
```
