# jaudiotagger — MP3 / Java

- **Pinned release:** `net.jthink:jaudiotagger:3.0.1`
- **License:** LGPL-2.1-or-later; pinned source `FileConstants.java` and embedded Maven POM headers specify 2.1 or later; published [POM](https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1.pom) declares LGPL
- **Parser family:** jaudiotagger's native MPEG frame-header parser; the same package/release already appears in the Java MP3-with-ID3v2 cell
- **Local byte API:** `MPEGFrameHeader.isMPEGFrame(ByteBuffer)` and `parseMPEGHeader(ByteBuffer)` on bytes read from a local untagged file
- **Documentation:** [MPEGFrameHeader API](https://www.jthink.net/jaudiotagger/javadoc/org/jaudiotagger/audio/mp3/MPEGFrameHeader.html) · [pinned release source](https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1-sources.jar)
- **Valid controls:** [`tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3) and [`tone-22k-stereo.mp3`](../../../../controls/mp3/tone-22k-stereo.mp3)
- **Evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [source lock](../../../../projects/mp3/java/jaudiotagger/source-lock.json) · [Docker verification](../../../../projects/mp3/java/jaudiotagger/verification.json) · [AFL++ feedback](../../../../data/java/mp3/jaudiotagger-feedback-differential.json)

The first control returns `{"codec":"MP3","mpeg_version":"MPEG-1","layer":"Layer 3","sample_rate":44100,"channels":1,"bitrate_kbps":64}`. The second returns MPEG-2 Layer III, 22,050 Hz, 2 channels, and 32 kbps. The adapter calls jaudiotagger's own `MPEGFrameHeader` parser on the four-byte header at byte zero. JaCoCo measures 221 source lines in `MPEGFrameHeader.java`. Three repeated primary-control AFL++ probes match, and the second valid control changes two parser-line features and two AFL++ tuple IDs. The release has no JLayer or JCodec runtime dependency.

**Limit:** This is a first-frame-header path, not a whole-file decoder. On the valid MPEG-2 control, the higher-level `MP3AudioHeader(File)` API misidentifies the audio start at byte 104 and estimates five frames; the independent control oracle says byte zero and 12 frames. `MPEGFrameHeader` also reports an incorrect MPEG-2 frame length and samples per frame, so those fields, duration, and total frame count are excluded from this path's observable result. No PCM, VBR, Xing/Info, ID3, or malformed-input behavior is established.

## Run

```sh
python3 parsarium.py build mp3 java jaudiotagger
python3 parsarium.py run mp3 java jaudiotagger controls/mp3/tone-44k-mono.mp3
```
