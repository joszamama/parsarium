# jave-core — ASCII PNM / Java

- **Pinned release:** `4.2.0`
- **License:** GPL-3.0-only
- **Parsed scope:** ASCII P3 PPM demuxer format and dimensions
- **Underlying family:** JAVE2 wrapper over bundled FFmpeg PPM decoder
- **Local input API:** `new MultimediaObject(File localPpm).getInfo().getVideo().getSize()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "format": "ppm_pipe",
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/jave_core/README.md)

```sh
python3 parsarium.py build ascii_pnm java jave_core
python3 parsarium.py run ascii_pnm java jave_core controls/ascii_pnm/red-green.ppm
```
