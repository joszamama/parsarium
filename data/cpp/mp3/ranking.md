# CPP × MP3: selected parsers

10 control-verified third-party paths selected from 10 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Homebrew installs (365 days) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | ID3v2 title and identified MP3 audio stream | FFmpeg libavformat MP3 demuxer and ID3v2 metadata reader |
| 2 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | ID3v2 title, MP3 audio track codec and duration from local tagged file | libmpv local media frontend over FFmpeg libavformat and libavcodec |
| 3 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | ID3v2 title plus one parsed MPEG audio stream with sample rate and channels | GStreamer id3demux and mpegaudioparse plugins via GstDiscoverer |
| 4 | [sox](https://sourceforge.net/p/sox/code/ci/master/tree/src/example0.c) | 14.4.2 | 28,127 | MP3 audio parsing and one decoded sample from a valid ID3v2-tagged input; ID3v2 text is not exposed | libsox MP3 handler over libmad decoder |
| 5 | [sdl_mixer](https://wiki.libsdl.org/SDL2_mixer/Mix_LoadMUS) | 2.8.2 | 15,365 | ID3v2 title and artist plus a 1-second MP3 music duration | SDL2_mixer ID3v2 tag reader and vendored minimp3 MP3 decoder |
| 6 | [mpg123](https://www.mpg123.org/api/group__mpg123__metadata.shtml) | 1.33.7 | 12,297 | ID3v2 title/version after scanning valid MP3 audio | libmpg123 MPEG audio and ID3v2 parser |
| 7 | [libsndfile](https://libsndfile.github.io/libsndfile/api.html) | 1.2.2 | 9,161 | ID3v2 title, MPEG Layer III sample rate/channels/frame count, and one decoded audio frame | libsndfile MPEG frontend over libmpg123 decoder and ID3v2 reader |
| 8 | [lame](https://github.com/lameproject/lame/blob/master/include/lame.h) | 4.0 | 6,924 | MP3 frame header and 576 decoded PCM samples from ID3v2-tagged local bytes; tag text is not exposed | LAME HIP decoder interface over libmpg123 |
| 9 | [taglib](https://taglib.org/api/) | 2.3.2 | 4,111 | ID3v2 title and artist from a valid tagged MP3 | TagLib ID3v2 parser |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | [Debian installations (popcon)](https://sources.debian.org/src/vlc/) | 68,409 | ID3v2 title and recognized MP3 audio track from valid local tagged MP3 | VLC media parser with bundled TagLib and MPEG audio plugins |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
