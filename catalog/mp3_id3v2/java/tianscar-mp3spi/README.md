# tianscar-mp3spi — MP3 with ID3v2 / Java

- **Pinned release:** `1.9.8`
- **License:** LGPL-2.0-only
- **Parsed scope:** local tagged MP3 type, ID3v2 title, artist, album and tag version
- **Underlying family:** Tianscar fork of JavaZOOM MP3SPI over JLayer and Tritonus
- **Local input API:** `new MpegAudioFileReader().getAudioFileFormat(File).properties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/tianscar/javasound/javasound-mp3/1.9.8/javasound-mp3-1.9.8-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "type": "MP3",
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "tag_version": "3"
}
```

Its source MpegAudioFileReader differs from the soundlibs MP3SPI release but preserves the same JavaZOOM parser lineage and public API.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
