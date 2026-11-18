# mp3spi — MP3 / Java

- **Pinned release:** `1.9.5.4`
- **Upstream:** [source repository](<https://github.com/pdudits/soundlibs>) · [Maven Central](<https://central.sonatype.com/artifact/com.googlecode.soundlibs/mp3spi>)
- **License:** LGPL-2.0-or-later
- **Parsed scope:** local tagged MP3 type, ID3v2 title, artist, album and tag version
- **Underlying family:** soundlibs MP3SPI Java Sound provider over its JLayer fork
- **Local input API:** `new MpegAudioFileReader().getAudioFileFormat(File).properties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/mp3spi/README.md)

```sh
python3 parsarium.py build mp3 java mp3spi
python3 parsarium.py run mp3 java mp3spi controls/mp3/id3v2-tagged-tone.mp3
```
