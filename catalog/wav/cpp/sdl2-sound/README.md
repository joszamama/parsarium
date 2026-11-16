# sdl2_sound — WAV / C++

- **Pinned release:** `2.0.6`
- **License:** Zlib AND (Artistic-1.0-Perl OR LGPL-2.1-or-later)
- **Parsed scope:** WAV decoder identified as Microsoft WAVE; parsed sample rate, channels, frames and four PCM samples
- **Underlying family:** SDL2_sound WAVE decoder
- **Local input API:** `Sound_NewSampleFromFile(local WAV path, NULL, 4096); Sound_DecodeAll; Sound_FreeSample`
- **Documentation:** [API reference](<https://icculus.org/SDL_sound/docs/html/SDL__sound_8h.html>)
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

SDL2_sound ships an internal WAVE decoder in the SDL_sound upstream family. SDL2_sound and SDL3_sound are separate major-version packages/APIs but share decoder lineage and upstream star count. This Homebrew binary links sdl2-compat and macOS AudioToolbox; the adapter observed its Microsoft WAVE decoder. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/sdl2_sound/README.md)

```sh
python3 parsarium.py build wav cpp sdl2_sound
python3 parsarium.py run wav cpp sdl2_sound controls/wav/four-samples.wav
```
