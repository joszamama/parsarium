# vlc — MP4 / C++

- **Pinned release:** `3.0.24`
- **Upstream:** [source repository](<https://code.videolan.org/videolan/vlc>) · [Debian](<https://tracker.debian.org/pkg/vlc>)
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** MP4 title, video/audio tracks and one-second duration
- **Underlying family:** VLC native MP4 demuxer plugin
- **Local input API:** `libvlc_media_new_path(local filename); libvlc_media_parse_with_options; libvlc_media_get_meta/tracks_get`
- **Documentation:** [API reference](<https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "video_tracks": 1,
  "audio_tracks": 1,
  "duration_ms": 1000
}
```

C and C++ call sites share libVLC and its bundled MP4 demuxer; exact plugin selection during this run was not independently traced.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/vlc/README.md)

```sh
python3 parsarium.py build mp4 cpp vlc
python3 parsarium.py run mp4 cpp vlc controls/mp4/red-av.mp4
```
