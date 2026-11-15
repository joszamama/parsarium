# bramp-ffmpeg — ASCII PNM / Java

- **Pinned release:** `0.9.2`
- **License:** BSD-2-Clause
- **Parsed scope:** ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream
- **Underlying family:** bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(String localExecutable).probe(String localPpm).getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar>)
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
