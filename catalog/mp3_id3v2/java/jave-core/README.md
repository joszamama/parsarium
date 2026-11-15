# jave-core — MP3 with ID3v2 / Java

- **Pinned release:** `4.2.0`
- **License:** GPL-3.0-only
- **Parsed scope:** local tagged MP3 format, codec, sample rate and channels
- **Underlying family:** JAVE2 wrapper over bundled FFmpeg MP3 demuxer
- **Local input API:** `new MultimediaObject(File).getInfo().getAudio()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3 (mp3float)",
  "frequency": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
