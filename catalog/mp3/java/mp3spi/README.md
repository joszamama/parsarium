# mp3spi — MP3 / Java

- **Pinned release:** `com.googlecode.soundlibs:mp3spi:1.9.5.4`
- **License:** LGPL-2.0-or-later, from the pinned `MpegAudioFileReader.java` and `DecodedMpegAudioInputStream.java` headers (Maven Central metadata says LGPL 2.1)
- **Parser family:** JavaZoom JLayer via MP3SPI Java Sound provider and the soundlibs JLayer 1.0.1.4 fork
- **Local input API:** `MpegAudioFileReader.getAudioInputStream(InputStream)` on a buffered local byte stream, then `MpegFormatConversionProvider.getAudioInputStream(PCM_SIGNED, encoded)` and read PCM to end
- **Documentation:** [Java SE AudioFileReader API](https://docs.oracle.com/en/java/javase/25/docs/api/java.desktop/javax/sound/sampled/spi/AudioFileReader.html) · [pinned MP3SPI source](https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar) · [Maven POM](https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4.pom)
- **Valid controls:** [`tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3) and [`tone-22k-stereo.mp3`](../../../../controls/mp3/tone-22k-stereo.mp3)
- **Evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [source lock](../../../../projects/mp3/java/mp3spi/source-lock.json) · [Docker verification](../../../../projects/mp3/java/mp3spi/verification.json) · [AFL++ feedback](../../../../data/java/mp3/mp3spi-feedback-differential.json)

The first control returns `{"codec":"MP3","sample_rate":44100,"channels":1,"frames":11,"decoded_samples":12672}`. The second returns 22,050 Hz, 2 channels, 12 frames, and 6,912 decoded samples per channel. MP3SPI's `MpegAudioFileReader` recognizes the stream and its `DecodedMpegAudioInputStream` converts it to PCM through soundlibs JLayer. JaCoCo measures MP3SPI source lines and soundlibs JLayer source lines separately; `LayerIIIDecoder.java` contributes 658 executed lines on the control. Across the two valid streams, the 220 MP3SPI wrapper lines are the same; all 242 differing source-line features come from the soundlibs JLayer core. The AFL++ bitmap differs by 240 tuple IDs.

The MP3SPI JAR registers `AudioFileReader` and `FormatConversionProvider` services, but the adapter constructs both classes directly. Java SE alone has no MP3 reader in the recorded inventory. MP3SPI is a distinct package and Java Sound API path that shares JLayer's Layer III decoder lineage with the selected `javazoom:jlayer` path. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, or ID3 behavior.

## Run

```sh
python3 parsarium.py build mp3 java mp3spi
python3 parsarium.py run mp3 java mp3spi controls/mp3/tone-44k-mono.mp3
```
