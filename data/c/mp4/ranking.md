# C × MP4: verified parser ranking

5 verified third-party package paths; working goal 20, ceiling 30. Formula install-on-request counts use the same 365-day window (2025-11-13 through 2026-11-13) within this ecosystem. They measure broad package requests, not MP4-specific use.

| Rank | Package | Pinned release | Homebrew requested installs | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html) | 9.0.2 | 1,763,198 | MP4 major brand, title, two tracks, 2x2 video dimensions | FFmpeg libavformat MOV/MP4 demuxer |
| 2 | [mpv](https://mpv.io/manual/stable/) | 0.42.0 | 91,258 | MP4 demuxer, title and H.264/AAC track codecs | libmpv over FFmpeg MOV/MP4 demuxer |
| 3 | [gstreamer](https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html) | 1.28.9 | 44,909 | MP4 title, video/audio streams and 2x2 video dimensions | GStreamer isomp4/qtdemux plugin |
| 4 | [libmediainfo](https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start) | 26.10 | 1,285 | MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions | MediaInfoLib native MPEG-4 parser |

| — | [vlc](https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html) | 3.0.24 | unavailable | MP4 title, video/audio tracks and one-second duration | VLC native MP4 demuxer plugin |

FFmpeg, GStreamer, MediaInfoLib and VLC expose distinct package APIs and MP4 demuxers. libmpv shares FFmpeg. VLC is distributed as a cask and has no comparable formula install-on-request count, so its order is unresolved. Five leads remain unresolved; 15 more verified paths are needed. See `cell.json`, `registry-snapshot.json`, `source-lock.json`, and `verification.json`.
