# jaffree — ASCII PNM / Java

- **Pinned release:** `2024.08.29`
- **Upstream:** [source repository](<https://github.com/kokorin/Jaffree>) · [Maven Central](<https://central.sonatype.com/artifact/com.github.kokorin.jaffree/jaffree>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream
- **Underlying family:** Jaffree wrapper over local FFprobe/FFmpeg
- **Local input API:** `FFprobe.atPath(Path localExecutableDir).setShowStreams(true).setInput(Path localPpm).execute().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/jaffree/README.md)

```sh
python3 parsarium.py build ascii_pnm java jaffree
python3 parsarium.py run ascii_pnm java jaffree controls/ascii_pnm/red-green.ppm
```
