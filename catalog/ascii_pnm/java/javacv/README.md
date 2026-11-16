# javacv — ASCII PNM / Java

- **Pinned release:** `1.5.14`
- **License:** Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception
- **Parsed scope:** ASCII P3 PPM decoded frame, codec and dimensions; pixel values not inspected
- **Underlying family:** JavaCV wrapper over native FFmpeg PPM decoder
- **Local input API:** `new FFmpegFrameGrabber(File localPpm).start(); grabImage(); getVideoCodec(); getImageWidth(); getImageHeight()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "codec": "ppm",
  "width": 2,
  "height": 1,
  "frame": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/javacv/README.md)

```sh
python3 parsarium.py build ascii_pnm java javacv
python3 parsarium.py run ascii_pnm java javacv controls/ascii_pnm/red-green.ppm
```
