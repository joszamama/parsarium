# ffmpeg — WAV / C

- **Pinned release:** `9.0.2`
- **Upstream:** [source repository](<https://github.com/FFmpeg/FFmpeg>) · [Conan Center](<https://conan.io/center/recipes/ffmpeg>)
- **License:** GPL-3.0-or-later
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** FFmpeg WAV demuxer and PCM decoder
- **Local input API:** `avformat_open_input(local WAV path); avformat_find_stream_info; av_read_frame; avcodec_send_packet and avcodec_receive_frame`
- **Documentation:** [API reference](<https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html>)
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

FFmpeg libavformat/libavcodec pair; installed Homebrew build is GPL-enabled.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/c/ffmpeg/README.md)

```sh
python3 parsarium.py build wav c ffmpeg
python3 parsarium.py run wav c ffmpeg controls/wav/four-samples.wav
```
