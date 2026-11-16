# old-isoparser — MP4 / Java

- **Pinned release:** `1.1.22`
- **License:** Apache-2.0
- **Parsed scope:** movie track count and timescale
- **Underlying family:** older CoreMedia/sannies MP4Parser ISO BMFF parser
- **Local input API:** `new com.coremedia.iso.IsoFile(String localMp4Path), getMovieBox().getTrackCount() and getMovieHeaderBox().getTimescale()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/googlecode/mp4parser/isoparser/1.1.22/isoparser-1.1.22-javadoc.jar>)
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

[Docker harness and verification receipt](../../../../projects/mp4/java/old_isoparser/README.md)

```sh
python3 parsarium.py build mp4 java old_isoparser
python3 parsarium.py run mp4 java old_isoparser controls/mp4/red-av.mp4
```
