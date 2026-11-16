# @uttori/audio-wave — WAV / JavaScript

- **Pinned release:** `2.1.0`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** uttori/audio-wave
- **Local input API:** `AudioWAV.fromFile(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@uttori/audio-wave>)
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

[Docker harness and verification receipt](../../../../projects/wav/javascript/uttori_audio_wave/README.md)

```sh
python3 parsarium.py build wav javascript uttori_audio_wave
python3 parsarium.py run wav javascript uttori_audio_wave controls/wav/four-samples.wav
```
