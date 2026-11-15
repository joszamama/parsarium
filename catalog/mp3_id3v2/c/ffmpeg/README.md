# ffmpeg — MP3 with ID3v2 / C

- **Pinned release:** `9.0.2`
- **License:** GPL-3.0-or-later
- **Parsed scope:** ID3v2 title and identified MP3 audio stream
- **Underlying family:** FFmpeg libavformat MP3 demuxer and ID3v2 metadata reader
- **Local input API:** `avformat_open_input(local filename); avformat_find_stream_info; format metadata title and MP3 stream codec`
- **Documentation:** [API reference](<https://ffmpeg.org/doxygen/trunk/group__lavf__decoding.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "mp3_streams": 1
}
```

The same FFmpeg libavformat C demuxer serves C and C++ call sites. It identifies the MP3 audio stream and parses ID3v2 title metadata.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
