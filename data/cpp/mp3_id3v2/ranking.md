# C++ × MP3 with ID3v2: verified parser ranking

9 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts use one 365-day window (2025-11-13 through 2026-11-13) within this ecosystem. They measure broad formula requests, not MP3-specific use.

| Rank | Package | Pinned release | Homebrew requested installs | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | ID3v2 title and identified MP3 audio stream | FFmpeg libavformat MP3 demuxer and ID3v2 metadata reader |
| 2 | [sox](https://sourceforge.net/p/sox/code/ci/master/tree/src/example0.c) | 14.4.2 | 28,127 | MP3 audio handler and one decoded sample on tagged input | libsox over libmad |
| 3 | [sdl_mixer](https://wiki.libsdl.org/SDL2_mixer/Mix_LoadMUS) | 2.8.2 | 15,365 | ID3v2 title and artist, MP3 duration | SDL2_mixer tag reader over mpg123 audio decoder |
| 4 | [mpg123](https://www.mpg123.org/api/group__mpg123__metadata.shtml) | 1.33.7 | 12,297 | ID3v2 title/version after scanning valid MP3 audio | libmpg123 MPEG audio and ID3v2 parser |
| 5 | [libsndfile](https://libsndfile.github.io/libsndfile/api.html) | 1.2.2 | 9,161 | ID3v2 title, MP3 stream info and one decoded frame | libsndfile over mpg123 |
| 6 | [taglib](https://taglib.org/api/) | 2.3.2 | 4,111 | ID3v2 title and artist from a valid tagged MP3 | TagLib ID3v2 parser |
| 7 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | ID3v2 title, MPEG Audio format and sample rate | MediaInfoLib MPEG audio and ID3v2 parsers |
| 8 | [libid3tag](https://codeberg.org/tenacityteam/libid3tag/src/tag/0.16.4/include/id3tag.h.in) | 0.16.4 | 479 | ID3v2 title and normalized tag version/frame count | libid3tag ID3v2 metadata parser |
| 9 | [id3lib](https://id3lib.sourceforge.net/api/index.html) | 3.8.3 | 199 | ID3v2 title and frame count | id3lib C++ tag parser |

TagLib and id3lib C bindings use their C++ cores; libsndfile shares mpg123 for MP3 and ID3v2 parsing; MediaInfoLib uses its own format parsers and links ZenLib for utilities. SDL_mixer uses its own ID3v2 tag reader and shares mpg123 for MP3 audio. SoX uses libmad for audio and does not expose the control title. The other C and C++ call sites share their respective C libraries. libid3tag parses tags without decoding MP3 audio. Two leads remain unresolved, and 11 more verified paths are needed. See `cell.json`, `registry-snapshot.json`, and `verification.json`.
