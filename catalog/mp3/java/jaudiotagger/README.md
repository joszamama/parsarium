# jaudiotagger — MP3 / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.0.1`
- **License:** LGPL-2.1-or-later
- **Parser family:** jaudiotagger native MP3 and ID3v2 reader
- **Local input API:** `MPEGFrameHeader.isMPEGFrame(ByteBuffer) and parseMPEGHeader(ByteBuffer) on bytes read from an untagged local File; getters for MPEG version, layer, sampling rate, channel count and bitrate`
- **Documentation:** [API reference](<https://www.jthink.net/jaudiotagger/javadoc/org/jaudiotagger/audio/mp3/MPEGFrameHeader.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control result](../../../../data/java/mp3/verification.json)

## Observed control result

```json
{
  "codec": "MP3",
  "mpeg_version": "MPEG-1",
  "layer": "Layer 3",
  "sample_rate": 44100,
  "channels": 1,
  "bitrate_kbps": 64
}
```

## Run this target

```sh
python3 parsarium.py build mp3 java jaudiotagger
python3 parsarium.py run mp3 java jaudiotagger controls/mp3/tone-44k-mono.mp3
```
