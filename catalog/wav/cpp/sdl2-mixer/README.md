# sdl2_mixer — WAV / C++

- **Pinned release:** `2.8.2`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus four decoded PCM samples at configured mixer format
- **Underlying family:** SDL2_mixer through SDL2 compatibility and SDL WAV loader
- **Local input API:** `SDL_Init audio; Mix_OpenAudio; Mix_LoadWAV(local WAV path); Mix_QuerySpec; Mix_Chunk.abuf and alen`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2_mixer/Mix_LoadWAV>)
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

Same SDL_mixer upstream project as SDL3_mixer but distinct 2.x package/API. On this macOS build it links sdl2-compat, which uses SDL3 underneath; no independent WAV engine is claimed. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
