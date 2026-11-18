# sdl_mixer — MP3 / C

- **Pinned release:** `2.8.2`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL_mixer>)
- **License:** Zlib
- **Parsed scope:** ID3v2 title and artist plus a 1-second MP3 music duration
- **Underlying family:** SDL2_mixer ID3v2 tag reader and vendored minimp3 MP3 decoder
- **Local input API:** `Mix_Init(MIX_INIT_MP3); Mix_OpenAudio(dummy device); Mix_LoadMUS(local filename); Mix_GetMusicType/Mix_GetMusicTitleTag/Mix_GetMusicArtistTag/Mix_MusicDuration`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2_mixer/Mix_LoadMUS>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "duration_ms": 1000
}
```

The Parsarium harness builds the pinned SDL2_mixer with SDL2MIXER_MP3_MINIMP3=ON and SDL2MIXER_MP3_MPG123=OFF, so music_minimp3.c (vendored minimp3) decodes the audio after mp3_read_tags from mp3utils.c reads the tag; Debian's packaged SDL2_mixer, used for the original catalog check, links libmpg123 through music_mpg123.c instead. C and C++ adapters use the same SDL2_mixer C API. SDL3_mixer is another major release of the same upstream package and is not separately counted.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/c/sdl_mixer/README.md)

```sh
python3 parsarium.py build mp3 c sdl_mixer
python3 parsarium.py run mp3 c sdl_mixer controls/mp3/id3v2-tagged-tone.mp3
```
