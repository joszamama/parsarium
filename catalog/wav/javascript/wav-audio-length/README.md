# wav-audio-length — WAV / JavaScript

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** wav-audio-length
- **Local input API:** `duration(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/wav-audio-length>)
- **Catalog evidence:** [parser record](../../../../data/javascript/wav/parsers.json) · [control verification](../../../../data/javascript/wav/verification.json) · [within-ecosystem ranking](../../../../data/javascript/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "durationSeconds": 0.0005
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/javascript/wav_audio_length/README.md)

```sh
python3 parsarium.py build wav javascript wav_audio_length
python3 parsarium.py run wav javascript wav_audio_length controls/wav/four-samples.wav
```
