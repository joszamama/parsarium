# mp3spi — MP3 with ID3v2 / Java

- **Pinned release:** `1.9.5.4`
- **License:** LGPL-2.0-or-later
- **Parsed scope:** local tagged MP3 type, ID3v2 title, artist, album and tag version
- **Underlying family:** soundlibs MP3SPI Java Sound provider over its JLayer fork
- **Local input API:** `new MpegAudioFileReader().getAudioFileFormat(File).properties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
