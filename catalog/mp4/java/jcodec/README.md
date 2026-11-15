# jcodec — MP4 / Java

- **Pinned release:** `0.2.5`
- **License:** BSD-2-Clause
- **Parsed scope:** track count and video dimensions
- **Underlying family:** JCodec MP4 box parser
- **Local input API:** `MP4Util.parseMovie(File localMp4), MovieBox.getTracks() and TrakBox.getCodedSize()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video_width": 2,
  "video_height": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
