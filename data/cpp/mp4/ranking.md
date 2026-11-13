# C++ × MP4: verified parser ranking

18 verified third-party package paths; working goal 20, ceiling 30. Formula install-on-request counts use the same 365-day window (2025-11-13 through 2026-11-13) within this ecosystem. They measure broad package requests, not MP4-specific use.

| Rank | Package | Pinned release | Homebrew requested installs | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [libheif](https://github.com/strukturag/libheif/wiki/Reading-and-Writing-Sequences) | 1.23.7 | 91,937 | MP4 video sequence track and 2x2 resolution; audio ignored | libheif native ISO BMFF parser |
| 3 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 4 | [OpenCV](https://docs.opencv.org/5.0/main_modules/classcv_1_1VideoCapture.html) | 5.1.0 | 68,439 | MP4 video dimensions, frame count and frame rate | OpenCV VideoCapture over FFmpeg MOV/MP4 demuxer |
| 5 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 6 | [gpac](https://doxygen.gpac.io/group__isogen__grp.html) | 26.07.0 | 7,814 | two ISO media tracks, 2x2 video dimensions and duration | GPAC native ISO media parser |
| 7 | [TagLib](https://taglib.org/api/) | 2.3.2 | 4,021 | MP4 title and one-second duration | TagLib native MP4 metadata parser |
| 8 | [Exiv2](https://exiv2.org/doc/classExiv2_1_1QuickTimeVideo.html) | 0.28.9 | 2,425 | MP4 major brand and 2x2 video dimensions | Exiv2 native QuickTime/MP4 metadata parser |
| 9 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions | MediaInfoLib native MPEG-4 parser |
| 10 | [mp4v2](https://github.com/enzo1982/mp4v2/blob/v2.1.3/include/mp4v2/file.h) | 2.1.3 | 644 | two MP4 tracks and 2x2 video dimensions | MP4v2 native MP4 atom parser |
| 11 | [libextractor](https://www.gnu.org/software/libextractor/manual/extractor.html) | 1.20 | 164 | MP4 title, duration and 2x2 video dimensions | GNU libextractor qt plugin |
| 12 | [libquicktime](https://libquicktime.sourceforge.net/introduction.html) | 1.2.4 | 100 | two MP4 tracks and 2x2 video dimensions | libquicktime native QuickTime/MP4 atom reader |
| — | [bento4](https://github.com/axiomatic-systems/Bento4/blob/v1.6.0-641/Source/C%2B%2B/CApi/Bento4C.h) | 1.6.0-641 | unavailable | MP4 major brand, two audio/video tracks and one-second duration | Bento4 AP4 ISO BMFF core |
| — | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | unavailable | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |
| — | [AvCpp](https://h4tr3d.github.io/avcpp/formatcontext_8h_source.html) | 3.0.1 | unavailable | MP4 demuxer, one video and one audio stream | C++ wrapper over FFmpeg MOV/MP4 demuxer |
| — | [shiguredo/mp4-rs](https://github.com/shiguredo/mp4-rs/blob/2026.3.0/crates/c-api/README.md) | 2026.3.0 | unavailable | two tracks, one video, one audio, one-second video duration | Rust ISO BMFF demuxer through C API |
| — | [ireader/media-server](https://github.com/ireader/media-server/blob/v1.0.0/libmov/include/mov-reader.h) | 1.0.0 | unavailable | one video and one audio track, 2x2 dimensions and 1000 ms duration | ireader libmov native ISO BMFF/MOV reader |
| — | [libmp4tag](https://libmp4tag.sourceforge.io/) | 2.0.4 | unavailable | MP4 title and 1128 ms duration | libmp4tag native MP4 atom and tag parser |

MP4v2, GPAC, Bento4, FFmpeg, GStreamer, MediaInfoLib, libquicktime, libextractor, TagLib, Exiv2, libmp4tag, ireader libmov and VLC expose distinct package APIs and MP4 parsers. libmpv, OpenCV and AvCpp share FFmpeg. MP4Box is an alias for GPAC, and mp4ff supplies a Go API rather than a native library API. VLC is a cask, while Bento4, AvCpp, libmp4tag and ireader/media-server have no Homebrew formula in the bounded name search; none has a comparable formula install-on-request count. libquicktime, libextractor, TagLib, OpenCV, Exiv2, AvCpp and libmp4tag came from targeted project documentation; OpenCV verified container properties without decoding a frame. Two leads remain unresolved: qtmultimedia returned no format-specific control result and minimp4 has no pinnable upstream release; 2 more verified paths are needed. See `cell.json`, `registry-snapshot.json`, `source-lock.json`, and `verification.json`.

libmp4tag is a genuine published C parser release that passed the control, but it is unranked because its SourceForge downloads are not comparable to Homebrew formula install-on-request counts. The C++ path uses the same C parser.

AvCpp is unranked in the Homebrew metric. Its 543 project-wide GitHub stars are auxiliary and cannot be mixed into the formula ranking.

The tagged MIT `ireader/media-server` v1.0.0 `libmov` API passed the local MP4 control in both ecosystems through one native parser family. Its 3,529 GitHub stars are an auxiliary project-interest signal, not a Homebrew requested-install count, so it remains unranked. `lieff/minimp4` has a documented MP4 callback API and 441 stars but no upstream tag or release; it remains a lead.

The tagged Apache-2.0 `shiguredo/mp4-rs` 2026.3.0 release passed the local MP4 control through its published C API. Both ecosystem paths share the Rust demuxer. Its 158 project-wide GitHub stars are auxiliary; no comparable Homebrew formula count exists, so it remains unranked.

libheif 1.23.7 passed the valid MP4 control through its published sequence API, reporting the video track and 2x2 resolution while ignoring audio. Its 91,937 Homebrew requested installs place it second within this cell, measuring broad formula use rather than MP4-specific use. The C and C++ paths share one native parser.
