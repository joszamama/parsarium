# gstreamer — WAV / C

- **Pinned release:** `1.28.9`
- **Upstream:** [source repository](<https://gitlab.freedesktop.org/gstreamer/gstreamer>) · [Debian](<https://tracker.debian.org/pkg/gstreamer1.0>)
- **License:** LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
- **Parsed scope:** explicit wavparse element interprets WAV and emits caps plus four PCM sample values
- **Underlying family:** GStreamer wavparse plugin
- **Local input API:** `gst_parse_launch(filesrc local path ! wavparse ! appsink); gst_app_sink_try_pull_sample`
- **Documentation:** [API reference](<https://gstreamer.freedesktop.org/documentation/wavparse/index.html>)
- **Catalog evidence:** [parser record](../../../../data/c/wav/parsers.json) · [control verification](../../../../data/c/wav/verification.json) · [within-ecosystem ranking](../../../../data/c/wav/ranking.md)
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

GStreamer Good Plug-ins wavparse handles WAV; the adapter explicitly uses the named plugin and reads parsed caps and PCM from appsink. It is a separate package path, with plugin binary and release checked. Its primary upstream is GitLab, so no GitHub-star score is borrowed from a mirror.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/c/gstreamer/README.md)

```sh
python3 parsarium.py build wav c gstreamer
python3 parsarium.py run wav c gstreamer controls/wav/four-samples.wav
```
