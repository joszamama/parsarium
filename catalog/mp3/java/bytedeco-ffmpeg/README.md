# bytedeco-ffmpeg — MP3 / Java

- **Pinned release:** `8.1.2-1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** local tagged MP3 format, sample rate and channels
- **Underlying family:** Bytedeco binding to the same FFmpeg MP3 demuxer used by JavaCV
- **Local input API:** `avformat_open_input(AVFormatContext,String,...), avformat_find_stream_info(...), AVStream.codecpar()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "frequency": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/bytedeco_ffmpeg/README.md)

```sh
python3 parsarium.py build mp3 java bytedeco_ffmpeg
python3 parsarium.py run mp3 java bytedeco_ffmpeg controls/mp3/id3v2-tagged-tone.mp3
```
