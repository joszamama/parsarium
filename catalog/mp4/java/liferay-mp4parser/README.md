# liferay-mp4parser — MP4 / Java

- **Pinned release:** `1.9.41.2.LIFERAY-PATCHED-2`
- **License:** LGPL-2.1-only
- **Parsed scope:** movie track count and timescale
- **Underlying family:** Liferay-patched distribution of sannies MP4Parser ISO BMFF parser
- **Local input API:** `new org.mp4parser.IsoFile(File localMp4), getMovieBox().getTrackCount() and getMovieHeaderBox().getTimescale()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/liferay/org.mp4parser/1.9.41.2.LIFERAY-PATCHED-2/org.mp4parser-1.9.41.2.LIFERAY-PATCHED-2-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "timescale": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
