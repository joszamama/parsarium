# C × MP4: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Homebrew installs (365 days) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [libheif](https://github.com/strukturag/libheif/wiki/Reading-and-Writing-Sequences) | 1.23.7 | 91,937 | MP4 video sequence track and 2x2 image resolution; the library does not expose the audio track through this sequence API | libheif native ISO BMFF image-sequence and MP4 parser |
| 3 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 4 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 5 | [gpac](https://doxygen.gpac.io/group__isogen__grp.html) | 26.07.0 | 7,814 | two ISO media tracks, 2x2 video dimensions and duration | GPAC native ISO media parser |
| 6 | [taglib](https://github.com/taglib/taglib/blob/v2.3.2/bindings/c/tag_c.h) | 2.3.2 | 4,021 | MP4 title metadata and one-second duration | TagLib native MP4 metadata parser |
| 7 | [bento4](https://github.com/axiomatic-systems/Bento4/blob/v1.6.0-641/Source/C%2B%2B/CApi/Bento4C.h) | 1.6.0-641 | 2,325 | MP4 major brand, two audio/video tracks and one-second duration | Bento4 AP4 ISO BMFF core |
| 8 | [mlt](https://mltframework.org/docs/framework/) | 7.42.0 | 1,526 | AVFormat producer parsed MP4 video/audio codecs and 2x2 video dimensions | MLT avformat producer over FFmpeg MOV/MP4 demuxer |
| 9 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions | MediaInfoLib native MPEG-4 parser |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | [Debian installations (popcon)](https://sources.debian.org/src/vlc/) | 68,409 | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
