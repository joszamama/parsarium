# CPP × WAV: selected parsers

10 control-verified third-party paths selected from 22 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub stars of primary upstream repository.

| Rank | Package | Release | GitHub stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,107 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | FFmpeg WAV demuxer and PCM decoder |
| 2 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,640 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | raylib bundled dr_wav decoder |
| 3 | [sdl2](https://wiki.libsdl.org/SDL2/SDL_LoadWAV) | 2.32.10 | 16,973 | WAV sample rate, channel and frame counts, plus four decoded PCM samples | native SDL2 WAV reader |
| 4 | [sdl3](https://wiki.libsdl.org/SDL3/SDL_LoadWAV) | 3.4.20 | 16,973 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | SDL3 WAV loader |
| 5 | [sfml](https://github.com/SFML/SFML/blob/3.0.2/include/SFML/Audio/SoundBuffer.hpp) | 3.0.2 | 12,105 | WAV sample rate, channels, frame count and four decoded PCM samples | SFML audio sound-file decoder |
| 6 | [miniaudio](https://github.com/mackron/miniaudio/blob/0.11.26/miniaudio.h) | 0.11.26 | 7,616 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | miniaudio bundled dr_wav decoder |
| 7 | [aubio](https://github.com/aubio/aubio/blob/0.4.9/src/io/source.h) | 0.4.9 | 3,787 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | aubio source abstraction |
| 8 | [allegro](https://liballeg.org/a5docs/5.2.11.3/acodec.html) | 5.2.11.3 | 2,133 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | Allegro audio codec WAV loader |
| 9 | [dr_wav](https://github.com/mackron/dr_libs/blob/wav-0.14.6/dr_wav.h) | wav-0.14.6 | 1,891 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | dr_wav C WAV decoder |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [gstreamer](https://gstreamer.freedesktop.org/documentation/wavparse/index.html) | 1.28.9 | [Debian installations (popcon)](https://sources.debian.org/src/gstreamer1.0/) | 172,612 | explicit wavparse element interprets WAV and emits caps plus four PCM sample values | GStreamer wavparse plugin |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
