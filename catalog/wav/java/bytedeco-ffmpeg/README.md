# bytedeco-ffmpeg — WAV / Java

- **Pinned release:** `8.1.2-1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** WAV format, sample rate and channels
- **Underlying family:** Bytedeco binding to FFmpeg demuxer
- **Local input API:** `avformat_open_input(AVFormatContext,String,...), avformat_find_stream_info(...) and AVStream.codecpar()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/bytedeco_ffmpeg/README.md)

```sh
python3 parsarium.py build wav java bytedeco_ffmpeg
python3 parsarium.py run wav java bytedeco_ffmpeg controls/wav/256-samples.wav
```
