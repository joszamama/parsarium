# ffmpeg — MP4 / C++

- **Pinned release:** `9.0.2`
- **License:** GPL-3.0-or-later
- **Parsed scope:** MP4 major brand, title, two tracks, 2x2 video dimensions
- **Underlying family:** FFmpeg libavformat MOV/MP4 demuxer
- **Local input API:** `avformat_open_input(local filename); avformat_find_stream_info; av_dict_get; AVStream.codecpar`
- **Documentation:** [API reference](<https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "title": "Parsarium",
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2
}
```

C and C++ call sites share libavformat; the MP4 box parser is in the MOV demuxer.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/ffmpeg/README.md)

```sh
python3 parsarium.py build mp4 cpp ffmpeg
python3 parsarium.py run mp4 cpp ffmpeg controls/mp4/red-av.mp4
```
