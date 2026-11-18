# ffmpeg — MP3 / C++

- **Pinned release:** `9.0.2`
- **Upstream:** [source repository](<https://github.com/FFmpeg/FFmpeg>) · [Debian](<https://tracker.debian.org/pkg/ffmpeg>)
- **License:** GPL-3.0-or-later
- **Parsed scope:** ID3v2 title and identified MP3 audio stream
- **Underlying family:** FFmpeg libavformat MP3 demuxer and ID3v2 metadata reader
- **Local input API:** `avformat_open_input(local filename); avformat_find_stream_info; format metadata title and MP3 stream codec`
- **Documentation:** [API reference](<https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3/parsers.json) · [control verification](../../../../data/cpp/mp3/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "mp3_streams": 1
}
```

The same FFmpeg libavformat C demuxer serves C and C++ call sites. It identifies the MP3 audio stream and parses ID3v2 title metadata.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/cpp/ffmpeg/README.md)

```sh
python3 parsarium.py build mp3 cpp ffmpeg
python3 parsarium.py run mp3 cpp ffmpeg controls/mp3/id3v2-tagged-tone.mp3
```
