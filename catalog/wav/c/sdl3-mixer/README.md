# sdl3_mixer — WAV / C

- **Pinned release:** `3.2.4`
- **License:** Zlib
- **Parsed scope:** parsed audio sample rate, channel count and duration in frames
- **Underlying family:** SDL3_mixer WAV decoder
- **Local input API:** `MIX_Init; MIX_LoadAudio(NULL, local WAV path, true); MIX_GetAudioFormat; MIX_GetAudioDuration; MIX_DestroyAudio`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3_mixer/MIX_LoadAudio>)
- **Catalog evidence:** [parser record](../../../../data/c/wav/parsers.json) · [control verification](../../../../data/c/wav/verification.json) · [within-ecosystem ranking](../../../../data/c/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4
}
```

Dedicated src/decoder_wav.c in the pinned release derives from SDL2_mixer music_wav.c and earlier SDL_wave.c; related SDL lineage but separate from SDL3 core LoadWAV implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
