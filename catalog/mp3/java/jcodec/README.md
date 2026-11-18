# jcodec — MP3 / Java

- **Pinned release:** `0.2.5`
- **Upstream:** [source repository](<https://github.com/jcodec/jcodec>) · [Maven Central](<https://central.sonatype.com/artifact/org.jcodec/jcodec>)
- **License:** BSD-2-Clause
- **Parsed scope:** first MP3 audio frame codec, byte length and timescale from local tagged MP3
- **Underlying family:** JCodec native MPEG audio demuxer
- **Local input API:** `new MPEGAudioDemuxer(NIOUtils.readableChannel(File)).getAudioTracks().get(0).nextFrame()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "codec": "MP3",
  "frame_bytes": 288,
  "timescale": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/jcodec/README.md)

```sh
python3 parsarium.py build mp3 java jcodec
python3 parsarium.py run mp3 java jcodec controls/mp3/id3v2-tagged-tone.mp3
```
