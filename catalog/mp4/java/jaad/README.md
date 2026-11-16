# jaad — MP4 / Java

- **Pinned release:** `0.8.7`
- **License:** Public Domain
- **Parsed scope:** MP4 track count, AAC codec, sample rate and channels
- **Underlying family:** JAAD pure Java MP4 demultiplexer
- **Local input API:** `new MP4Container(RandomAccessFile localMp4).getMovie().getTracks(), AudioTrack.getSampleRate() and getChannelCount()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/de/sfuhrm/jaad/0.8.7/jaad-0.8.7-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av-no-udta.mp4`](../../../../controls/mp4/red-av-no-udta.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "audio_codec": "AAC",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/jaad/README.md)

```sh
python3 parsarium.py build mp4 java jaad
python3 parsarium.py run mp4 java jaad controls/mp4/red-av-no-udta.mp4
```
