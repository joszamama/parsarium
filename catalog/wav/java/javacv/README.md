# javacv — WAV / Java

- **Pinned release:** `1.5.14`
- **Upstream:** [source repository](<https://github.com/bytedeco/javacv>) · [Maven Central](<https://central.sonatype.com/artifact/org.bytedeco/javacv>)
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** WAV format, PCM codec, sample rate and channels
- **Underlying family:** JavaCV wrapper over FFmpeg demuxer
- **Local input API:** `new FFmpegFrameGrabber(File).start(), getFormat(), getAudioCodecName(), getSampleRate(), getAudioChannels()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "codec": "pcm_s16le",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/javacv/README.md)

```sh
python3 parsarium.py build wav java javacv
python3 parsarium.py run wav java javacv controls/wav/256-samples.wav
```
