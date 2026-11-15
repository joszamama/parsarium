# muxer — MP4 / Java

- **Pinned release:** `1.9.56`
- **License:** Apache-2.0
- **Parsed scope:** video and audio track handlers
- **Underlying family:** sannies MP4Parser movie builder over isoparser
- **Local input API:** `MovieCreator.build(String localMp4Path), Movie.getTracks() and Track.getHandler()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/mp4parser/muxer/1.9.56/muxer-1.9.56-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "handlers": [
    "vide",
    "soun"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
