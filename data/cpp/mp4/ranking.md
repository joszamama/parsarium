# CPP × MP4: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Homebrew installs (365 days) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [libheif](https://github.com/strukturag/libheif/wiki/Reading-and-Writing-Sequences) | 1.23.7 | 91,937 | MP4 video sequence track and 2x2 image resolution; the library does not expose the audio track through this sequence API | libheif native ISO BMFF image-sequence and MP4 parser |
| 3 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 4 | [opencv](https://github.com/opencv/opencv/blob/5.1.0/modules/videoio/include/opencv2/videoio.hpp) | 5.1.0 | 68,439 | MP4 video dimensions, frame count and frame rate from FFmpeg-backed VideoCapture | OpenCV VideoCapture wrapper over FFmpeg MOV/MP4 demuxer |
| 5 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 6 | [gpac](https://doxygen.gpac.io/group__isogen__grp.html) | 26.07.0 | 7,814 | two ISO media tracks, 2x2 video dimensions and duration | GPAC native ISO media parser |
| 7 | [taglib](https://taglib.org/api/) | 2.3.2 | 4,021 | MP4 title metadata and one-second duration | TagLib native MP4 metadata parser |
| 8 | [exiv2](https://exiv2.org/doc/classExiv2_1_1QuickTimeVideo.html) | 0.28.9 | 2,425 | MP4 major brand and video dimensions from parsed QuickTime XMP metadata | Exiv2 native QuickTime/MP4 metadata parser |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | [Debian installations (popcon)](https://sources.debian.org/src/vlc/) | 68,409 | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |
| 2 | [libopenshot](https://github.com/OpenShot/libopenshot/blob/v1.1.1/src/FFmpegReader.h) | 1.1.1 | [Debian installations (popcon)](https://sources.debian.org/src/libopenshot/) | 2,560 | FFmpegReader opened a valid MP4, reporting H.264 video, AAC audio and 2x2 dimensions | OpenShot FFmpegReader over FFmpeg MOV/MP4 demuxer |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
