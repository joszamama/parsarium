# mpv — MP4 / C

- **Pinned release:** `0.42.0`
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

C and C++ call sites share libmpv, which links the FFmpeg package already listed directly.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
