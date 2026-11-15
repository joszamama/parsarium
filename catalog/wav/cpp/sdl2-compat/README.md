# sdl2-compat — WAV / C++

- **Pinned release:** `2.32.74`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus four decoded PCM samples
- **Underlying family:** SDL2 compatibility layer over SDL3 WAV loader
- **Local input API:** `SDL_LoadWAV(local WAV path, SDL_AudioSpec*, Uint8**, Uint32*); SDL_FreeWAV`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2/SDL_LoadWAV>)
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

Separate SDL2-compat release/package offering SDL2 C API while using SDL3 internally; same underlying WAV parser family as SDL3 core, counted as a package path only. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
