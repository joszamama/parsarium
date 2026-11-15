# bramp-ffmpeg — MP3 with ID3v2 / Java

- **Pinned release:** `0.9.2`
- **License:** BSD-2-Clause
- **Parsed scope:** local tagged MP3 format, codec, sample rate, channels and title
- **Underlying family:** bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(String localExecutable).probe(String localMp3).getStreams(), getFormat().getTags()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3",
  "frequency": 8000,
  "channels": 1,
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
