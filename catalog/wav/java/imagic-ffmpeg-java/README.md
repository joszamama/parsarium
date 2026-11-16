# imagic-ffmpeg-java — WAV / Java

- **Pinned release:** `0.1.2`
- **License:** BSD-2-Clause
- **Parsed scope:** WAV format, PCM codec, sample rate and channels
- **Underlying family:** Imagic fork of bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(Executor,File localExecutable).probe(File localWav).get()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar>)
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

[Docker harness and verification receipt](../../../../projects/wav/java/imagic_ffmpeg_java/README.md)

```sh
python3 parsarium.py build wav java imagic_ffmpeg_java
python3 parsarium.py run wav java imagic_ffmpeg_java controls/wav/256-samples.wav
```
