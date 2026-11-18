# sdl3 — WAV / C++

- **Pinned release:** `3.4.20`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL>)
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** SDL3 WAV loader
- **Local input API:** `SDL_LoadWAV(local WAV path, SDL_AudioSpec*, Uint8**, Uint32*); SDL_free decoded PCM buffer`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3/SDL_LoadWAV>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
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

SDL3 core WAV-specific loading API; separate package and parser path from SDL_mixer, which remains unresolved. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/sdl3/README.md)

```sh
python3 parsarium.py build wav cpp sdl3
python3 parsarium.py run wav cpp sdl3 controls/wav/four-samples.wav
```
