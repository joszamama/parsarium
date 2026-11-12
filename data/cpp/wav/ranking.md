# C++ × WAV: verified parser ranking

22 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured between 2026-11-12T10:25:21.715408+00:00 and 2026-11-12T11:32:40.616429+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C++, and do not establish a complete most-used set. 2 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C++ standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,107 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | FFmpeg WAV demuxer and PCM decoder |
| 2 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,640 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | raylib bundled dr_wav decoder |
| 3 | [sdl2](https://wiki.libsdl.org/SDL2/SDL_LoadWAV) | 2.32.10 | 16,973 | WAV sample rate, channel and frame counts, plus four decoded PCM samples | native SDL2 WAV reader |
| 3 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadWAV) | 3.4.20 | 16,973 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | SDL3 WAV loader |
| 5 | [sfml](https://github.com/SFML/SFML/blob/3.0.2/include/SFML/Audio/SoundBuffer.hpp) | 3.0.2 | 12,105 | WAV sample rate, channels, frame count and four decoded PCM samples | SFML audio sound-file decoder |
| 6 | [miniaudio](https://github.com/mackron/miniaudio/blob/0.11.26/miniaudio.h) | 0.11.26 | 7,616 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | miniaudio bundled dr_wav decoder |
| 7 | [aubio](https://github.com/aubio/aubio/blob/0.4.9/src/io/source.h) | 0.4.9 | 3,787 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | aubio source abstraction |
| 8 | [allegro](https://liballeg.org/a5docs/5.2.11.3/acodec.html) | 5.2.11.3 | 2,133 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | Allegro audio codec WAV loader |
| 9 | [dr_wav](https://github.com/mackron/dr_libs/blob/wav-0.14.6/dr_wav.h) | wav-0.14.6 | 1,891 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | dr_wav C WAV decoder |
| 10 | [libsndfile](https://libsndfile.github.io/libsndfile/api.html) | 1.2.2 | 1,732 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | libsndfile WAV decoder |
| 11 | [taglib](https://github.com/taglib/taglib/blob/v2.3.2/bindings/c/tag_c.h) | 2.3.2 | 1,470 | WAV-aware structural/audio-property parsing; does not decode PCM samples | TagLib C bindings over TagLib C++ RIFF/WAV parser |
| 12 | [audiofile](https://github.com/adamstark/AudioFile/blob/1.1.4/README.md) | 1.1.4 | 1,150 | WAV sample rate, channels, frame count and four decoded PCM samples | adamstark AudioFile WAV parser |
| 13 | [sdl2_mixer](https://wiki.libsdl.org/SDL2_mixer/Mix_LoadWAV) | 2.8.2 | 765 | WAV sample rate, channel and frame counts, plus four decoded PCM samples at configured mixer format | SDL2_mixer through SDL2 compatibility and SDL WAV loader |
| 13 | [sdl3_mixer](https://wiki.libsdl.org/SDL3_mixer/MIX_LoadAudio) | 3.2.4 | 765 | parsed audio sample rate, channel count and duration in frames | SDL3_mixer WAV decoder |
| 15 | [csfml](https://github.com/SFML/CSFML/blob/3.0.0/include/CSFML/Audio/SoundBuffer.h) | 3.0.0 | 382 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | CSFML C facade over SFML audio |
| 16 | [sdl2-compat](https://wiki.libsdl.org/SDL2/SDL_LoadWAV) | 2.32.74 | 221 | WAV sample rate, channel and frame counts, plus four decoded PCM samples | SDL2 compatibility layer over SDL3 WAV loader |
| 17 | [sdl2_sound](https://icculus.org/SDL_sound/docs/html/SDL__sound_8h.html) | 2.0.6 | 182 | WAV decoder identified as Microsoft WAVE; parsed sample rate, channels, frames and four PCM samples | SDL2_sound WAVE decoder |
| 17 | [sdl3_sound](https://wiki.icculus.org/SDL3_sound/Sound_NewSampleFromFile) | 3.2.0 | 182 | WAV decoder identified as Microsoft WAVE; parsed sample rate, channels, frames and four PCM samples | SDL3_sound WAVE decoder |
| 19 | [libaudiofile](https://github.com/mpruett/audiofile/blob/audiofile-0.3.6/libaudiofile/audiofile.h) | 0.3.6 | 167 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | Audio File Library WAV parser |
| 20 | [freealut](https://github.com/vancegroup/freealut/blob/freealut_1_1_0/include/AL/alut.h) | 1.1.0 | 74 | WAV format, sample rate, frame count and four decoded PCM samples | FreeALUT WAV memory loader |
| unranked | [gstreamer](https://gstreamer.freedesktop.org/documentation/wavparse/index.html) | 1.28.9 | unknown | explicit wavparse element interprets WAV and emits caps plus four PCM sample values | GStreamer wavparse plugin |
| unranked | [sox](https://github.com/chirlu/sox/blob/master/libsox.3) | 14.4.2 | unknown | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | SoX libsox WAV reader |
