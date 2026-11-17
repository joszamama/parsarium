# jcodec — MP3 / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.2.5`
- **License:** BSD-2-Clause
- **Parser family:** JCodec native MPEG audio demuxer
- **Local input API:** `new MPEGAudioDemuxer(NIOUtils.readableChannel(File)).getAudioTracks().get(0).nextFrame() until null; new Mp3Decoder().getCodecMeta(ByteBuffer) and decodeFrame(ByteBuffer, ByteBuffer) per frame`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control result](../../../../data/java/mp3/verification.json)

## Observed control result

```json
{
  "codec": "MP3",
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "decoded_samples": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 java jcodec
python3 parsarium.py run mp3 java jcodec controls/mp3/tone-44k-mono.mp3
```
