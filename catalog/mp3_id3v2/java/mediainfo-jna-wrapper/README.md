# mediainfo-jna-wrapper — MP3 with ID3v2 / Java

- **Pinned release:** `2.1.9`
- **License:** MIT + MediaInfoLib Binary License
- **Parsed scope:** local 72,941-byte tagged MP3 format, sample rate, channels and title
- **Underlying family:** amilesend JNA binding to libmediainfo
- **Local input API:** `new MediaInfo(new MediaInfoAccessor(MediaInfoLibrary.newInstance())).open(File localMp3).get(StreamType,int,String)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-long.mp3`](../../../../controls/mp3_id3v2/tone-tags-long.mp3)

## Observed control result

```json
{
  "format": "MPEG Audio",
  "frequency": 8000,
  "channels": 1,
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
