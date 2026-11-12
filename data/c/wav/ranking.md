# C × WAV: verified parser ranking

14 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured between 2026-11-12T10:25:21.715408+00:00 and 2026-11-12T10:52:52.681242+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 1 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,107 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | FFmpeg WAV demuxer and PCM decoder |
| 2 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,640 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | raylib bundled dr_wav decoder |
| 3 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadWAV) | 3.4.20 | 16,973 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | SDL3 WAV loader |
| 4 | [miniaudio](https://github.com/mackron/miniaudio/blob/0.11.26/miniaudio.h) | 0.11.26 | 7,616 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | miniaudio bundled dr_wav decoder |
| 5 | [aubio](https://github.com/aubio/aubio/blob/0.4.9/src/io/source.h) | 0.4.9 | 3,787 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | aubio source abstraction |
| 6 | [allegro](https://liballeg.org/a5docs/5.2.11.3/acodec.html) | 5.2.11.3 | 2,133 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | Allegro audio codec WAV loader |
| 7 | [dr_wav](https://github.com/mackron/dr_libs/blob/wav-0.14.6/dr_wav.h) | wav-0.14.6 | 1,891 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | dr_wav C WAV decoder |
| 8 | [libsndfile](https://libsndfile.github.io/libsndfile/api.html) | 1.2.2 | 1,732 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | libsndfile WAV decoder |
| 9 | [sdl2_mixer](https://wiki.libsdl.org/SDL2_mixer/Mix_LoadWAV) | 2.8.2 | 765 | WAV sample rate, channel and frame counts, plus four decoded PCM samples at configured mixer format | SDL2_mixer through SDL2 compatibility and SDL WAV loader |
| 9 | [sdl3_mixer](https://wiki.libsdl.org/SDL3_mixer/MIX_LoadAudio) | 3.2.4 | 765 | parsed audio sample rate, channel count and duration in frames | SDL3_mixer WAV decoder |
| 11 | [csfml](https://github.com/SFML/CSFML/blob/3.0.0/include/CSFML/Audio/SoundBuffer.h) | 3.0.0 | 382 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | CSFML C facade over SFML audio |
| 12 | [libaudiofile](https://github.com/mpruett/audiofile/blob/audiofile-0.3.6/libaudiofile/audiofile.h) | 0.3.6 | 167 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | Audio File Library WAV parser |
| 13 | [freealut](https://github.com/vancegroup/freealut/blob/freealut_1_1_0/include/AL/alut.h) | 1.1.0 | 74 | WAV format, sample rate, frame count and four decoded PCM samples | FreeALUT WAV memory loader |
| unranked | [sox](https://github.com/chirlu/sox/blob/master/libsox.3) | 14.4.2 | unknown | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | SoX libsox WAV reader |
