# javacv — MP4 / Java

- **Pinned release:** `1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** MP4 demuxer format, video dimensions, AAC sample rate and channels
- **Underlying family:** JavaCV wrapper over FFmpeg demuxer
- **Local input API:** `new FFmpegFrameGrabber(File localMp4).start(), getFormat(), getImageWidth(), getImageHeight(), getSampleRate(), getAudioChannels()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mov,mp4,m4a,3gp,3g2,mj2",
  "width": 2,
  "height": 2,
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
