# imagic-ffmpeg-java — MP3 with ID3v2 / Java

- **Pinned release:** `0.1.2`
- **License:** BSD-2-Clause
- **Parsed scope:** local tagged MP3 format, codec, sample rate, channels and title
- **Underlying family:** Imagic fork of bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(Executor,File localExecutable).probe(File localMp3).get(), getStreams(), getFormat().getTags()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/java/imagic_ffmpeg_java/README.md)

```sh
python3 parsarium.py build mp3_id3v2 java imagic_ffmpeg_java
python3 parsarium.py run mp3_id3v2 java imagic_ffmpeg_java controls/mp3_id3v2/tone-tags.mp3
```
