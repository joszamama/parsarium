# javasound-aac — MP4 / Java

- **Pinned release:** `0.9.8`
- **License:** Apache-2.0
- **Parsed scope:** MP4 track count, AAC codec, sample rate and channels
- **Underlying family:** Tianscar fork of JAAD pure Java MP4 demultiplexer
- **Local input API:** `MP4InputStream.open(FileInputStream localMp4), new MP4Container(MP4InputStream).getMovie().getTracks()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/tianscar/javasound/javasound-aac/0.9.8/javasound-aac-0.9.8-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

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

[Docker harness and verification receipt](../../../../projects/mp4/java/javasound_aac/README.md)

```sh
python3 parsarium.py build mp4 java javasound_aac
python3 parsarium.py run mp4 java javasound_aac controls/mp4/red-av.mp4
```
