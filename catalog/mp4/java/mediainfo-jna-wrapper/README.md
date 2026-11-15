# mediainfo-jna-wrapper — MP4 / Java

- **Pinned release:** `2.1.9`
- **License:** MIT + MediaInfoLib Binary License
- **Parsed scope:** MP4 format, video dimensions and audio sample rate
- **Underlying family:** amilesend JNA binding to libmediainfo
- **Local input API:** `new MediaInfo(new MediaInfoAccessor(MediaInfoLibrary.newInstance())).open(File localMp4).get(StreamType.Video,0,String)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av-padded.mp4`](../../../../controls/mp4/red-av-padded.mp4)

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
