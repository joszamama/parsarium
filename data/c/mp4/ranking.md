# C × MP4: verified parser ranking

19 verified third-party package paths; working goal 20, ceiling 30. Formula install-on-request counts use the same 365-day window (2025-11-13 through 2026-11-13) within this ecosystem. They measure broad package requests, not MP4-specific use.

| Rank | Package | Pinned release | Homebrew requested installs | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [libheif](https://github.com/strukturag/libheif/wiki/Reading-and-Writing-Sequences) | 1.23.7 | 91,937 | MP4 video sequence track and 2x2 resolution; audio ignored | libheif native ISO BMFF parser |
| 3 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 4 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 5 | [gpac](https://doxygen.gpac.io/group__isogen__grp.html) | 26.07.0 | 7,814 | two ISO media tracks, 2x2 video dimensions and duration | GPAC native ISO media parser |
| 6 | [TagLib](https://taglib.org/api/) | 2.3.2 | 4,021 | MP4 title and one-second duration | TagLib native MP4 metadata parser |
| 7 | [bento4](https://github.com/axiomatic-systems/Bento4/blob/v1.6.0-641/Source/C%2B%2B/CApi/Bento4C.h) | 1.6.0-641 | 2,325 | MP4 major brand, two audio/video tracks and one-second duration | Bento4 AP4 ISO BMFF core |
| 8 | [MLT](https://mltframework.org/plugins/ProducerAvformat/) | 7.42.0 | 1,526 | two streams, H.264/AAC codecs and 2x2 video dimensions | MLT avformat plugin over FFmpeg MOV/MP4 demuxer |
| 9 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions | MediaInfoLib native MPEG-4 parser |
| 10 | [mp4v2](https://github.com/enzo1982/mp4v2/blob/v2.1.3/include/mp4v2/file.h) | 2.1.3 | 644 | two MP4 tracks and 2x2 video dimensions | MP4v2 native MP4 atom parser |
| 11 | [libextractor](https://www.gnu.org/software/libextractor/manual/extractor.html) | 1.20 | 164 | MP4 title, duration and 2x2 video dimensions | GNU libextractor qt plugin |
| 12 | [libquicktime](https://libquicktime.sourceforge.net/introduction.html) | 1.2.4 | 100 | two MP4 tracks and 2x2 video dimensions | libquicktime native QuickTime/MP4 atom reader |
| — | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | unavailable | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |
| — | [shiguredo/mp4-rs](https://github.com/shiguredo/mp4-rs/blob/2026.3.0/crates/c-api/README.md) | 2026.3.0 | unavailable | two tracks, one video, one audio, one-second video duration | Rust ISO BMFF demuxer through C API |
| — | [ireader/media-server](https://github.com/ireader/media-server/blob/v1.0.0/libmov/include/mov-reader.h) | 1.0.0 | unavailable | one video and one audio track, 2x2 dimensions and 1000 ms duration | ireader libmov native ISO BMFF/MOV reader |
| — | [libmp4tag](https://libmp4tag.sourceforge.io/) | 2.0.4 | unavailable | MP4 title and 1128 ms duration | libmp4tag native MP4 atom and tag parser |
| — | [Mozilla mp4parse_capi](https://docs.rs/mp4parse_capi/0.17.0/mp4parse_capi/) | 0.17.0 | unavailable | two tracks, video/audio types and 2×2 video dimensions | Mozilla mp4parse Rust ISO BMFF parser through C API |
| — | [L-SMASH](https://github.com/l-smash/l-smash/blob/v2.14.5/lsmash.h) | 2.14.5 | unavailable | two tracks, video/audio types, 2×2 video display and 1000 ms duration | L-SMASH native ISO BMFF/MP4 box parser |
| — | [Libav](https://github.com/libav/libav/blob/v12.3/libavformat/avformat.h) | 12.3 | unavailable | ISO brand, two tracks, video/audio types and 2×2 dimensions | Libav MOV/MP4 demuxer, historical FFmpeg fork |

MP4v2, GPAC, Bento4, FFmpeg, GStreamer, MediaInfoLib, libquicktime, libextractor, TagLib, libmp4tag, Mozilla mp4parse_capi, ireader libmov, L-SMASH and VLC expose distinct package APIs and MP4 parsers. Libav is a separately released fork with FFmpeg ancestry, and libmpv shares the currently pinned FFmpeg parser. MP4Box is an alias for GPAC, and mp4ff supplies a Go API rather than a native library API. VLC is a cask, while libmp4tag, Mozilla mp4parse_capi, ireader/media-server, L-SMASH and Libav have no comparable Homebrew formula install-on-request count. The Bento4 formula stable version matches the pinned 1.6.0-641 release; 2,325 requested installs place it seventh in this cell. The four initial Homebrew name queries missed this formula, so formula absence can no longer be inferred from those windows. libquicktime, libextractor, TagLib, libmp4tag, Mozilla mp4parse_capi, L-SMASH and Libav came from targeted project documentation and passed the control without codec decode plugins. One high-interest minimp4 lead remains unresolved for lack of a pinned release; 1 more verified path is needed. See `cell.json`, `registry-snapshot.json`, `source-lock.json`, and `verification.json`.

L-SMASH 2.14.5 was built from its tagged ISC source. Its local C input API returned two tracks, video and audio handler types, 2×2 display dimensions and 1000 ms movie duration. The upstream repository had 251 GitHub stars on 2026-11-13, an auxiliary project-interest signal; no comparable Homebrew requested-install metric was available, so L-SMASH is unranked.

Libav 12.3 was source-built with its MOV/MP4 demuxer and local file protocol. The C API returned the ISO brand, two video/audio tracks and 2×2 dimensions from the valid MP4 control. Libav is a historical fork of FFmpeg: this is a separate package path and build, with related parser code. Its 1,156 GitHub stars are auxiliary only; no comparable Homebrew requested-install metric was available, so Libav is unranked.

Mozilla documents the Rust MP4 parser and its published C API as the family used for Firefox track metadata parsing. The pinned 0.17.0 crates.io release passed this control; the current Firefox revision may differ. Its 30,929 lifetime crates.io downloads are a separate auxiliary signal and cannot be inserted into the Homebrew 365-day ranking.

libmp4tag is a genuine published C parser release that passed the control, but it is unranked because its SourceForge downloads are not comparable to Homebrew formula install-on-request counts. The C++ path uses the same C parser.

The tagged MIT `ireader/media-server` v1.0.0 `libmov` API passed the local MP4 control in both ecosystems through one native parser family. Its 3,529 GitHub stars are an auxiliary project-interest signal, not a Homebrew requested-install count, so it remains unranked. `lieff/minimp4` has a documented MP4 callback API and 441 stars but no upstream tag or release; it remains a lead.

The tagged Apache-2.0 `shiguredo/mp4-rs` 2026.3.0 release passed the local MP4 control through its published C API. Both ecosystem paths share the Rust demuxer. Its 158 project-wide GitHub stars are auxiliary; no comparable Homebrew formula count exists, so it remains unranked.

libheif 1.23.7 passed the valid MP4 control through its published sequence API, reporting the video track and 2x2 resolution while ignoring audio. Its 91,937 Homebrew requested installs place it second within this cell, measuring broad formula use rather than MP4-specific use. The C and C++ paths share one native parser.

MLT 7.42.0 passed the MP4 control through its avformat producer in both C and C++. Its 1,526 Homebrew requested installs rank eighth within this cell, while its avformat plugin shares FFmpeg 9.0.2 parsing. The C++ adapter uses MLT++ from the same release.
