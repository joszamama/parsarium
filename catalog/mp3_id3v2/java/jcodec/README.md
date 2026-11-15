# jcodec — MP3 with ID3v2 / Java

- **Pinned release:** `0.2.5`
- **License:** BSD-2-Clause
- **Parsed scope:** first MP3 audio frame codec, byte length and timescale from local tagged MP3
- **Underlying family:** JCodec native MPEG audio demuxer
- **Local input API:** `new MPEGAudioDemuxer(NIOUtils.readableChannel(File)).getAudioTracks().get(0).nextFrame()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "codec": "MP3",
  "frame_bytes": 288,
  "timescale": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
