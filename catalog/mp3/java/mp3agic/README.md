# mp3agic — MP3 / Java

- **Pinned release:** `com.mpatric:mp3agic:0.9.1`
- **License:** MIT, from the pinned [Maven POM](https://repo.maven.apache.org/maven2/com/mpatric/mp3agic/0.9.1/mp3agic-0.9.1.pom)
- **Parser family:** mp3agic's own `Mp3File` and `MpegFrame` implementation; the same release/package appears in the Java MP3-with-ID3v2 cell
- **Local file API:** `new Mp3File(Path)` followed by `getVersion()`, `getLayer()`, `getSampleRate()`, `getChannelMode()`, and `getBitrate()`
- **Documentation:** [project API examples](https://github.com/mpatric/mp3agic/blob/master/readme.md) · [pinned release source](https://repo.maven.apache.org/maven2/com/mpatric/mp3agic/0.9.1/mp3agic-0.9.1-sources.jar)
- **Valid controls:** [`tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3) and [`tone-22k-stereo.mp3`](../../../../controls/mp3/tone-22k-stereo.mp3)
- **Evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [source lock](../../../../projects/mp3/java/mp3agic/source-lock.json) · [Docker verification](../../../../projects/mp3/java/mp3agic/verification.json) · [AFL++ differential](../../../../data/java/mp3/mp3agic-feedback-differential.json)

The first control returns `{"codec":"MP3","mpeg_version":"1.0","layer":"III","sample_rate":44100,"channel_mode":"Mono","bitrate_kbps":64}`. The second returns MPEG 2.0 Layer III, 22,050 Hz, joint stereo, and 32 kbps. These header fields agree with the independent frame walker. JaCoCo covers 219 mp3agic source lines: 128 in `Mp3File.java`, 80 in `MpegFrame.java`, and 11 in `BufferTools.java`. Three primary-control AFL++ probes match; the second valid stream changes 76 parser source-line features and 76 AFL++ tuple IDs. The release POM has no JLayer or JCodec runtime dependency. The tagged-MP3 mp3agic entry is the same package; jaudiotagger and jid3lib have historical project ancestry with mp3agic, without proof of identical MPEG parsing code.

**Limit:** `Mp3File(Path)` scans the full file but misidentifies the valid MPEG-2 control at byte 104 and reports 5 frames and 261 ms. The independent oracle finds byte zero, 12 frames, and approximately 313 ms. Start offset, frame count, duration, and PCM decoding are not claimed. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, or ID3 behavior.

## Run

```sh
python3 parsarium.py build mp3 java mp3agic
python3 parsarium.py run mp3 java mp3agic controls/mp3/tone-44k-mono.mp3
```
