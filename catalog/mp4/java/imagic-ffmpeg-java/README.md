# imagic-ffmpeg-java — MP4 / Java

- **Pinned release:** `0.1.2`
- **License:** BSD-2-Clause
- **Parsed scope:** MP4 demuxer format, H.264/AAC stream codecs, video dimensions and audio rate
- **Underlying family:** Imagic fork of bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(Executor,File localExecutable).probe(File localMp4).get().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mov,mp4,m4a,3gp,3g2,mj2",
  "video_codec": "h264",
  "width": 2,
  "height": 2,
  "audio_codec": "aac",
  "sample_rate": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/imagic_ffmpeg_java/README.md)

```sh
python3 parsarium.py build mp4 java imagic_ffmpeg_java
python3 parsarium.py run mp4 java imagic_ffmpeg_java controls/mp4/red-av.mp4
```
