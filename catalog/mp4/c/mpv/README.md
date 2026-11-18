# mpv — MP4 / C

- **Pinned release:** `0.42.0`
- **Upstream:** [source repository](<https://github.com/mpv-player/mpv>) · [Debian](<https://tracker.debian.org/pkg/mpv>)
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** MP4 demuxer, title and H.264/AAC track codecs
- **Underlying family:** libmpv over FFmpeg MOV/MP4 demuxer
- **Local input API:** `mpv_command(loadfile, local filename); mpv_wait_event(FILE_LOADED); mpv_get_property_string`
- **Documentation:** [API reference](<https://mpv.io/manual/stable/>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "container": "mov,mp4,m4a,3gp,3g2,mj2",
  "title": "Parsarium",
  "video_codec": "h264",
  "audio_codec": "aac"
}
```

The C and C++ call sites use the same libmpv 0.42.0 wrapper and FFmpeg 9.0.2 MOV/MP4 demuxer as the direct FFmpeg rows. Verified AFL feedback is scoped to FFmpeg mov.c and its MP4 helpers plus mpv demux_lavf.c. A parsed MP4 can have only video, only audio, or no media sample; absent track codec fields remain empty.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/c/mpv/README.md)

```sh
python3 parsarium.py build mp4 c mpv
python3 parsarium.py run mp4 c mpv controls/mp4/red-av.mp4
```
