# ffmpeg — ASCII PNM / C

- **Pinned release:** `9.0.2`
- **License:** GPL-3.0-or-later
- **Parsed scope:** P3 codec identification, dimensions, and two decoded RGB pixels
- **Underlying family:** FFmpeg native PNM decoder
- **Local input API:** `avformat_open_input(local PPM path); av_find_best_stream; av_read_frame; avcodec_send_packet and avcodec_receive_frame`
- **Documentation:** [API reference](<https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "codec": "ppm",
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

FFmpeg image2 demuxer passes PPM packets to the native PNM decoder; the C++ path uses the same FFmpeg C implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/ffmpeg/README.md)

```sh
python3 parsarium.py build ascii_pnm c ffmpeg
python3 parsarium.py run ascii_pnm c ffmpeg controls/ascii_pnm/red-green.ppm
```
