# imagic-ffmpeg-java — ASCII PNM / Java

- **Pinned release:** `0.1.2`
- **License:** BSD-2-Clause
- **Parsed scope:** ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream
- **Underlying family:** Imagic fork of bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(Executor,File localExecutable).probe(File localPpm).get().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "codec": "ppm",
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/imagic_ffmpeg_java/README.md)

```sh
python3 parsarium.py build ascii_pnm java imagic_ffmpeg_java
python3 parsarium.py run ascii_pnm java imagic_ffmpeg_java controls/ascii_pnm/red-green.ppm
```
