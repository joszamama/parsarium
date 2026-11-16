# sdl2_sound — MP3 with ID3v2 / C++

- **Pinned release:** `2.0.6`
- **License:** Zlib AND (Artistic-1.0-Perl OR LGPL-2.1-or-later)
- **Parsed scope:** Decoded MP3 PCM, stream fields and duration from tagged local MP3; no ID3v2 text
- **Underlying family:** SDL_sound over bundled dr_mp3/minimp3
- **Local input API:** `Sound_NewSampleFromFile(local filename, desired, buffer size); Sound_Decode; Sound_GetDuration`
- **Documentation:** [API reference](<https://github.com/icculus/SDL_sound/blob/v2.0.6/src/SDL_sound.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_bytes": 4096,
  "duration_ms": 1000
}
```

SDL_sound is a separate upstream package from SDL_mixer. Its MP3 decoder embeds dr_mp3, also used by miniaudio and represented directly by dr_libs. C and C++ adapters share the same engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/cpp/sdl2_sound/README.md)

```sh
python3 parsarium.py build mp3_id3v2 cpp sdl2_sound
python3 parsarium.py run mp3_id3v2 cpp sdl2_sound controls/mp3_id3v2/tone-tags.mp3
```
