# jave-core — MP4 / Java

- **Pinned release:** `4.2.0`
- **Upstream:** [source repository](<https://github.com/a-schild/jave2>) · [Maven Central](<https://central.sonatype.com/artifact/ws.schild/jave-core>)
- **License:** GPL-3.0-only
- **Parsed scope:** MP4 format, video dimensions, audio rate and channels
- **Underlying family:** JAVE2 wrapper over bundled FFmpeg
- **Local input API:** `new MultimediaObject(File localMp4).getInfo().getVideo() and getAudio()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mov",
  "width": 2,
  "height": 2,
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/jave_core/README.md)

```sh
python3 parsarium.py build mp4 java jave_core
python3 parsarium.py run mp4 java jave_core controls/mp4/red-av.mp4
```
