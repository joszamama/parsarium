# red5-io — MP4 / Java

- **Pinned release:** `2.0.40`
- **License:** Apache-2.0
- **Parsed scope:** MP4 video presence, parsed keyframe count and H.264/AAC codec identifiers
- **Underlying family:** Red5 MP4Reader over JCodec MP4 demuxer
- **Local input API:** `new MP4Reader(File localMp4), hasVideo(), analyzeKeyFrames().positions, getVideoCodecId() and getAudioCodecId()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/red5/red5-io/2.0.40/red5-io-2.0.40-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av-3s.mp4`](../../../../controls/mp4/red-av-3s.mp4)

## Observed control result

```json
{
  "video": true,
  "keyframes": 1,
  "video_codec": "avc1",
  "audio_codec": "mp4a"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/red5_io/README.md)

```sh
python3 parsarium.py build mp4 java red5_io
python3 parsarium.py run mp4 java red5_io controls/mp4/red-av-3s.mp4
```
