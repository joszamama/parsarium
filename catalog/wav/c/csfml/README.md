# csfml — WAV / C

- **Pinned release:** `3.0.0`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** CSFML C facade over SFML audio
- **Local input API:** `sfSoundBuffer_createFromFile(local WAV path); sfSoundBuffer_getSamples, getSampleCount, getSampleRate, getChannelCount`
- **Documentation:** [API reference](<https://github.com/SFML/CSFML/blob/3.0.0/include/CSFML/Audio/SoundBuffer.h>)
- **Catalog evidence:** [parser record](../../../../data/c/wav/parsers.json) · [control verification](../../../../data/c/wav/verification.json) · [within-ecosystem ranking](../../../../data/c/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

Official C binding around SFML SoundBuffer. The installed CSFML and SFML audio binaries are both SHA-256-checked; this shares SFML parser implementation rather than adding a new engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/c/csfml/README.md)

```sh
python3 parsarium.py build wav c csfml
python3 parsarium.py run wav c csfml controls/wav/four-samples.wav
```
