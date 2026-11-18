# bytedeco-ffmpeg — MP4 / Java

- **Pinned release:** `8.1.2-1.5.14`
- **Upstream:** [source repository](<https://github.com/bytedeco/javacpp-presets>) · [Maven Central](<https://central.sonatype.com/artifact/org.bytedeco/ffmpeg>)
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** MP4 demuxer format, two streams and video dimensions
- **Underlying family:** Bytedeco binding to FFmpeg demuxer
- **Local input API:** `avformat_open_input(AVFormatContext,String localMp4Path,...), avformat_find_stream_info(...) and AVStream.codecpar()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mov,mp4,m4a,3gp,3g2,mj2",
  "streams": 2,
  "width": 2,
  "height": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/bytedeco_ffmpeg/README.md)

```sh
python3 parsarium.py build mp4 java bytedeco_ffmpeg
python3 parsarium.py run mp4 java bytedeco_ffmpeg controls/mp4/red-av.mp4
```
