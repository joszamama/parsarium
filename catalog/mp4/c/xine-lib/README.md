# xine-lib — MP4 / C

- **Pinned release:** `1.2.13`
- **License:** GPL-2.0-or-later
- **Parsed scope:** native QuickTime/MP4 demuxer reports video/audio tracks and 2x2 video dimensions
- **Underlying family:** Xine native QuickTime/MP4 demux_qt parser
- **Local input API:** `xine_new; xine_init; xine_stream_new with dummy audio/video ports; xine_open(local MP4 path); xine_get_stream_info for video/audio and dimensions`
- **Documentation:** [API reference](<https://xine.sourceforge.net/releases.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "has_video": 1,
  "has_audio": 1,
  "width": 2,
  "height": 2
}
```

The source-built xineplug_dmx_video plugin includes demux_qt.c. FFmpeg decoding and avformat plugins are disabled for this control, so this is a separate MP4 parser family from FFmpeg and Libav.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
