# sdl3_sound — WAV / C++

- **Pinned release:** `3.2.0`
- **License:** Zlib AND (LGPL-2.1-or-later OR Artistic-1.0-Perl)
- **Parsed scope:** WAV decoder identified as Microsoft WAVE; parsed sample rate, channels, frames and four PCM samples
- **Underlying family:** SDL3_sound WAVE decoder
- **Local input API:** `Sound_NewSampleFromFile(local WAV path, NULL, 4096); Sound_DecodeAll; Sound_FreeSample`
- **Documentation:** [API reference](<https://wiki.icculus.org/SDL3_sound/Sound_NewSampleFromFile>)
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

sdl3-sound ships an internal WAVE decoder in the SDL_sound upstream family. SDL2_sound and SDL3_sound are separate major-version packages/APIs but share decoder lineage and upstream star count. This Homebrew binary links SDL3 and macOS AudioToolbox; the adapter observed its Microsoft WAVE decoder. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
