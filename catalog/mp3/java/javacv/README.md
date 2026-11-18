# javacv — MP3 / Java

- **Pinned release:** `1.5.14`
- **Upstream:** [source repository](<https://github.com/bytedeco/javacv>) · [Maven Central](<https://central.sonatype.com/artifact/org.bytedeco/javacv>)
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** local tagged MP3 format, codec, sample rate and channels
- **Underlying family:** JavaCV wrapper over FFmpeg MP3 demuxer
- **Local input API:** `new FFmpegFrameGrabber(File).start(), getFormat(), getAudioCodecName(), getSampleRate(), getAudioChannels()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "format": "mp3",
  "codec": "mp3float",
  "frequency": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/javacv/README.md)

```sh
python3 parsarium.py build mp3 java javacv
python3 parsarium.py run mp3 java javacv controls/mp3/id3v2-tagged-tone.mp3
```
