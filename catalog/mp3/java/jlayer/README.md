# jlayer — MP3 / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.1`
- **License:** LGPL-2.0-or-later
- **Parser family:** Original JavaZoom JLayer bitstream and Layer III decoder
- **Local input API:** `new Bitstream(FileInputStream(local File)); readFrame() and Decoder.decodeFrame(Header, Bitstream) for every Layer III frame; SampleBuffer.getBufferLength()`
- **Documentation:** [API reference](<https://javadoc.io/static/javazoom/jlayer/1.0.1/javazoom/jl/decoder/Bitstream.html>)
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
python3 parsarium.py build mp3 java jlayer
python3 parsarium.py run mp3 java jlayer controls/mp3/tone-44k-mono.mp3
```
