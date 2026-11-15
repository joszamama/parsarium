# gstreamer — WAV / C++

- **Pinned release:** `1.28.9`
- **License:** LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
- **Parsed scope:** explicit wavparse element interprets WAV and emits caps plus four PCM sample values
- **Underlying family:** GStreamer wavparse plugin
- **Local input API:** `gst_parse_launch(filesrc local path ! wavparse ! appsink); gst_app_sink_try_pull_sample`
- **Documentation:** [API reference](<https://gstreamer.freedesktop.org/documentation/wavparse/index.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

GStreamer Good Plug-ins wavparse handles WAV; the adapter explicitly uses the named plugin and reads parsed caps and PCM from appsink. It is a separate package path, with plugin binary and release checked. Its primary upstream is GitLab, so no GitHub-star score is borrowed from a mirror. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
