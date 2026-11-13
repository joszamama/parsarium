# C++ × MP4: verified parser ranking

12 verified third-party package paths; working goal 20, ceiling 30. Formula install-on-request counts use the same 365-day window (2025-11-13 through 2026-11-13) within this ecosystem. They measure broad package requests, not MP4-specific use.

| Rank | Package | Pinned release | Homebrew requested installs | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 3 | [OpenCV](https://docs.opencv.org/5.0/main_modules/classcv_1_1VideoCapture.html) | 5.1.0 | 68,439 | MP4 video dimensions, frame count and frame rate | OpenCV VideoCapture over FFmpeg MOV/MP4 demuxer |
| 4 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 5 | [gpac](https://doxygen.gpac.io/group__isogen__grp.html) | 26.07.0 | 7,814 | two ISO media tracks, 2x2 video dimensions and duration | GPAC native ISO media parser |
| 6 | [TagLib](https://taglib.org/api/) | 2.3.2 | 4,021 | MP4 title and one-second duration | TagLib native MP4 metadata parser |
| 7 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions | MediaInfoLib native MPEG-4 parser |
| 8 | [mp4v2](https://github.com/enzo1982/mp4v2/blob/v2.1.3/include/mp4v2/file.h) | 2.1.3 | 644 | two MP4 tracks and 2x2 video dimensions | MP4v2 native MP4 atom parser |
| 9 | [libextractor](https://www.gnu.org/software/libextractor/manual/extractor.html) | 1.20 | 164 | MP4 title, duration and 2x2 video dimensions | GNU libextractor qt plugin |
| 10 | [libquicktime](https://libquicktime.sourceforge.net/introduction.html) | 1.2.4 | 100 | two MP4 tracks and 2x2 video dimensions | libquicktime native QuickTime/MP4 atom reader |

| — | [bento4](https://github.com/axiomatic-systems/Bento4/blob/v1.6.0-641/Source/C%2B%2B/CApi/Bento4C.h) | 1.6.0-641 | unavailable | MP4 major brand, two audio/video tracks and one-second duration | Bento4 AP4 ISO BMFF core |
| — | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | unavailable | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |

MP4v2, GPAC, Bento4, FFmpeg, GStreamer, MediaInfoLib, libquicktime, libextractor, TagLib and VLC expose distinct package APIs and MP4 parsers. libmpv and OpenCV share FFmpeg. MP4Box is an alias for GPAC, and mp4ff supplies a Go API rather than a native library API. VLC is a cask and Bento4 has no Homebrew formula in the bounded name search; neither has a comparable formula install-on-request count. libquicktime, libextractor, TagLib and OpenCV came from targeted project documentation; OpenCV verified container properties without decoding a frame. No recorded documentation lead remains unresolved; 8 more verified paths are needed. See `cell.json`, `registry-snapshot.json`, `source-lock.json`, and `verification.json`.
