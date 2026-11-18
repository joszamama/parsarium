# isoparser — MP4 / Java

- **Pinned release:** `1.9.56`
- **Upstream:** [source repository](<https://github.com/sannies/mp4parser>) · [Maven Central](<https://central.sonatype.com/artifact/org.mp4parser/isoparser>)
- **License:** Apache-2.0
- **Parsed scope:** movie track count and timescale
- **Underlying family:** sannies MP4Parser ISO BMFF box parser
- **Local input API:** `new IsoFile(File localMp4), getMovieBox().getTrackCount() and getMovieHeaderBox().getTimescale()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "timescale": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/isoparser/README.md)

```sh
python3 parsarium.py build mp4 java isoparser
python3 parsarium.py run mp4 java isoparser controls/mp4/red-av.mp4
```
