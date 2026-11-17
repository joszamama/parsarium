# gstreamer — MP3 / C

- **Pinned release:** `1.28.9`
- **License:** LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
- **Parsed scope:** ID3v2 title plus one parsed MPEG audio stream with sample rate and channels
- **Underlying family:** GStreamer id3demux and mpegaudioparse plugins via GstDiscoverer
- **Local input API:** `gst_filename_to_uri(local filename); gst_discoverer_discover_uri; gst_discoverer_info_get_tags/audio_streams`
- **Documentation:** [API reference](<https://gstreamer.freedesktop.org/documentation/pbutils/gstdiscoverer.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "sample_rate": 8000,
  "channels": 1,
  "audio_streams": 1
}
```

The C and C++ call sites use the same GStreamer C API. GstDiscoverer invokes the pinned id3demux and MPEG audio parser plugins; the monorepo and installed plugin binaries are pinned.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/gstreamer/README.md)

```sh
python3 parsarium.py build mp3 c gstreamer
python3 parsarium.py run mp3 c gstreamer controls/mp3_id3v2/tone-tags.mp3
```
