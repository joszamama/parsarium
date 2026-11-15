# sdl2 — WAV / C

- **Pinned release:** `2.32.10`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus four decoded PCM samples
- **Underlying family:** native SDL2 WAV reader
- **Local input API:** `SDL_LoadWAV(local WAV path, SDL_AudioSpec*, Uint8**, Uint32*); SDL_FreeWAV, linked to source-built native SDL2`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2/SDL_LoadWAV>)
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

Official SDL2 2.32.10 source-built library, separate from sdl2-compat and SDL3 package paths; SDL WAV code lineage is shared across major versions. Same adapter C API is linked against this isolated native SDL2 binary.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
