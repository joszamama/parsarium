# vlcj-info — MP4 / Java

- **Pinned release:** `2.0.3`
- **License:** GPL-3.0-or-later
- **Parsed scope:** MP4 format, video dimensions and audio sample rate
- **Underlying family:** vlcj-info JNA binding to libmediainfo
- **Local input API:** `new MediaInfoFile(String localMp4).open(), info(String MediaInfo template)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/uk/co/caprica/vlcj-info/2.0.3/vlcj-info-2.0.3-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "MPEG-4",
  "width": 2,
  "height": 2,
  "sample_rate": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
