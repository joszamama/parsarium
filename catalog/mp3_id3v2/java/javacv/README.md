# javacv — MP3 with ID3v2 / Java

- **Pinned release:** `1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** local tagged MP3 format, codec, sample rate and channels
- **Underlying family:** JavaCV wrapper over FFmpeg MP3 demuxer
- **Local input API:** `new FFmpegFrameGrabber(File).start(), getFormat(), getAudioCodecName(), getSampleRate(), getAudioChannels()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3float",
  "frequency": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
