# bytedeco-ffmpeg — ASCII PNM / Java

- **Pinned release:** `8.1.2-1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** ASCII P3 PPM codec and dimensions parsed from stream
- **Underlying family:** Bytedeco binding to native FFmpeg PPM decoder
- **Local input API:** `avformat_open_input(AVFormatContext, String localPpmPath, ...); avformat_find_stream_info(...); AVStream.codecpar()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "codec": "ppm",
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
