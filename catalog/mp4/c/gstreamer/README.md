# gstreamer — MP4 / C

- **Pinned release:** `1.28.9`
- **License:** LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
- **Parsed scope:** MP4 title, video/audio streams and 2x2 video dimensions
- **Underlying family:** GStreamer isomp4/qtdemux plugin
- **Local input API:** `gst_filename_to_uri(local filename); gst_discoverer_discover_uri; gst_discoverer_info_get_video_streams/audio_streams`
- **Documentation:** [API reference](<https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2
}
```

C and C++ call sites share the pinned isomp4/qtdemux plugin.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
