# bytedeco-ffmpeg — MP3 with ID3v2 / Java

- **Pinned release:** `8.1.2-1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** local tagged MP3 format, sample rate and channels
- **Underlying family:** Bytedeco binding to the same FFmpeg MP3 demuxer used by JavaCV
- **Local input API:** `avformat_open_input(AVFormatContext,String,...), avformat_find_stream_info(...), AVStream.codecpar()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "frequency": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
