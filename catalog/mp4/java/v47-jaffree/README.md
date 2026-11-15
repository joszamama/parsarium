# v47-jaffree — MP4 / Java

- **Pinned release:** `2.1.0`
- **License:** GPL-3.0-only
- **Parsed scope:** MP4 H.264/AAC stream codecs, video dimensions and audio rate
- **Underlying family:** v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg
- **Local input API:** `FFprobe.atPath(Path localBin).setShowStreams(true).setInput(Path localMp4).execute().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "width": 2,
  "height": 2,
  "audio_codec": "aac",
  "sample_rate": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
