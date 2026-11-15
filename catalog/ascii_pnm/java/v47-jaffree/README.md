# v47-jaffree — ASCII PNM / Java

- **Pinned release:** `2.1.0`
- **License:** GPL-3.0-only
- **Parsed scope:** ASCII P3 PPM codec and 2x1 dimensions parsed from FFprobe stream
- **Underlying family:** v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg
- **Local input API:** `FFprobe.atPath(Path localBin).setShowStreams(true).setInput(Path localPpm).execute().getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
