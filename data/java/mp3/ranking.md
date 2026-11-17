# JAVA × MP3: selected parsers

5 control-verified third-party paths selected. The ceiling is ten and the list is not padded. JCodec, MP3SPI, and JLayer decode PCM; jaudiotagger is a first-frame-header parser and mp3agic reports only accurate header fields from its file scan. A path is a package/API route, not necessarily an independent decoder engine.

[JCodec](../../../projects/mp3/java/jcodec/README.md) 0.2.5 synchronizes and decodes each frame with its own Java code. [MP3SPI](../../../projects/mp3/java/mp3spi/README.md) 1.9.5.4 uses its `MpegAudioFileReader` and `DecodedMpegAudioInputStream` Java Sound path, then the soundlibs JLayer fork for frame decoding. [JLayer](../../../projects/mp3/java/jlayer/README.md) 1.0.1 uses `Bitstream`, `Header`, and `LayerIIIDecoder` directly. MP3SPI and JLayer are distinct package/API paths within the same decoder lineage; JCodec is an independent decoder family. [jaudiotagger](../../../projects/mp3/java/jaudiotagger/README.md) parses only the first MPEG frame header with its own Java code; it is the same package as its Java MP3-with-ID3v2 entry and has no JLayer or JCodec runtime dependency. [mp3agic](../../../projects/mp3/java/mp3agic/README.md) scans local files with its own `Mp3File` and `MpegFrame` code and reports only independently correct header fields.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). The single-release maximum is recorded as a cross-check. The count covers whole-package dependency use, not MP3 calls alone.

| Rank | Package | Release | Metric | Max single release | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [org.jcodec:jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | 0.2.5 | 76 | 44 (0.2.5) | Every frame of an untagged stream: codec, sample rate, channels, frames, decoded samples | JCodec native MPEG audio demuxer |
| 2 | [com.googlecode.soundlibs:mp3spi](https://central.sonatype.com/artifact/com.googlecode.soundlibs/mp3spi/1.9.5.4) | 1.9.5.4 | 55 | 38 (1.9.5.4) | Direct Java Sound reader and converter over every untagged Layer III frame, with PCM decode through soundlibs JLayer | JavaZoom JLayer via MP3SPI and soundlibs fork |
| 3 | [javazoom:jlayer](https://javadoc.io/static/javazoom/jlayer/1.0.1/javazoom/jl/decoder/Bitstream.html) | 1.0.1 | 33 | 33 (1.0.1) | Full Layer III frame and PCM sample decode from local InputStream | Original JavaZoom JLayer decoder |
| 4 | [net.jthink:jaudiotagger](https://www.jthink.net/jaudiotagger/javadoc/org/jaudiotagger/audio/mp3/MPEGFrameHeader.html) | 3.0.1 | 8 | 7 (3.0.1) | First four-byte Layer III frame header: version, layer, rate, channels, bitrate; no PCM or whole-stream claim | jaudiotagger native MPEG frame-header parser |
| 5 | [com.mpatric:mp3agic](https://github.com/mpatric/mp3agic/blob/master/readme.md) | 0.9.1 | 6 | 4 (0.9.1) | Local `Mp3File(Path)` scan: correct version, layer, rate, channel mode, bitrate; no accurate frame count/duration claim | mp3agic native MPEG frame-header parser |

Controls: `controls/mp3/tone-44k-mono.mp3` gives MP3, 44,100 Hz, 1 channel, 11 frames, 12,672 samples; the AFL++ differential `controls/mp3/tone-22k-stereo.mp3` gives 22,050 Hz, 2 channels, 12 frames, 6,912 samples. Both match the independent header walker and libmpg123 pilot. JaCoCo covers 1,142 JCodec and 1,724 JLayer source lines on the primary control. MP3SPI covers 220 of its own source lines, including 80 in `DecodedMpegAudioInputStream.java`, and separately 1,739 soundlibs JLayer lines including `LayerIIIDecoder.java`. The two valid streams produce distinct parser-derived AFL++ feedback in all five paths. For MP3SPI, the 220 wrapper lines are identical across controls while the soundlibs JLayer core differs by 242 source-line features and 240 AFL++ tuple IDs. jaudiotagger covers 221 lines in its own `MPEGFrameHeader.java`; the two controls differ by two source-line features and two AFL++ tuple IDs. mp3agic covers 219 own source lines (128 file scanner, 80 MPEG frame parser, 11 buffer helpers); the second control changes 76 source-line features and 76 AFL++ tuple IDs. Feedback receipts: [mp3agic](mp3agic-feedback-differential.json), [jaudiotagger](jaudiotagger-feedback-differential.json), [MP3SPI](mp3spi-feedback-differential.json), and [JLayer](jlayer-feedback-differential.json).

The low-level jaudiotagger API returns correct version, layer, rate, channels, and bitrate on both controls. Its higher-level `MP3AudioHeader(File)` incorrectly starts the MPEG-2 control at byte 104 and estimates five rather than 12 frames; `MPEGFrameHeader` also gives an incorrect MPEG-2 frame length and sample count. Those fields are not reported by the selected adapter. mp3agic also reports MPEG-2 start byte 104, 5 frames and 261 ms versus oracle byte zero, 12 frames and about 313 ms; its selected adapter excludes those fields too.

javacv (315) and org.bytedeco:ffmpeg (215) have higher counts but are JNI wrappers: MP3 parsing runs in native FFmpeg, with no Java parser source to cover. They are excluded here, not ranked.

JavaMP3 (4) is an MIT-licensed pure-Java decoder with a documented `Sound(InputStream)` API. Its release POM has no JLayer runtime dependency and the source JAR has no JavaZoom package or JLayer reference; broader code ancestry was not audited. Its 1.0.1 release decodes the 44.1 kHz mono control to the oracle's 12,672 samples, but crashes in `Decoder.samples_III` while constructing `Sound` from the valid 22.05 kHz stereo control. The [pinned Docker probe](probes/javamp3/README.md) records both outcomes. It fails the two-control gate and is excluded from ranking; no coverage or AFL++ feedback is claimed.

## Standard API (none)

OpenJDK 25.0.5 Java Sound without third-party providers has readers for WAV, AU and AIFF only; `AudioSystem.getAudioFileFormat` and `getAudioInputStream` throw `UnsupportedAudioFileException` on the primary control. Details in [standard.json](standard.json).

## Lead log

Looked up on deps.dev; selected entries are removed from this lead log.

| Lead | Version seen | Summed direct dependents | Max single release | Status | Note |
| --- | --- | ---: | ---: | --- | --- |
| [org.bytedeco:javacv](https://central.sonatype.com/artifact/org.bytedeco/javacv) | 1.5.14 | 315 | 69 | excluded_native_wrapper | FFmpegFrameGrabber is a JNI wrapper; MP3 frame parsing and decoding run in native FFmpeg (libavformat/libavcodec), so there are no Java parser source lines for JaCoCo. The C/FFmpeg family belongs to a native cell. Recorded as FFmpeg family in data/java/mp3_id3v2/parsers.json. |
| [org.bytedeco:ffmpeg](https://central.sonatype.com/artifact/org.bytedeco/ffmpeg) | 8.1.2-1.5.14 | 215 | 76 | excluded_native_wrapper | JavaCPP binding to the same native FFmpeg demuxer and decoder as javacv; no Java parser source. Not run. |
| [ws.schild:jave-core](https://central.sonatype.com/artifact/ws.schild/jave-core) | 4.2.0 | 52 | 9 | excluded_native_wrapper | Runs a bundled ffmpeg executable and parses its text output; parser is native FFmpeg. Not run. |
| [com.badlogicgames.jlayer:jlayer](https://central.sonatype.com/artifact/com.badlogicgames.jlayer/jlayer) | 1.0.2-gdx | 30 | 26 | unresolved_shared_family | libGDX repackaging of JLayer; same decoder family as javazoom:jlayer. Not run. |
| [com.googlecode.soundlibs:jlayer](https://central.sonatype.com/artifact/com.googlecode.soundlibs/jlayer) | 1.0.1.4 | 28 | 14 | unresolved_shared_family | Maintained fork of javazoom JLayer; same decoder family as javazoom:jlayer. Not run. |
| [com.soywiz:korau-mp3](https://central.sonatype.com/artifact/com.soywiz/korau-mp3) | 0.19.1 | 25 | 2 | unresolved | Kotlin korau MP3 decoder module published to Maven (last release 0.19.1); decoder lineage not inspected. Control not run. |
| [fr.delthas:javamp3](https://github.com/delthas/JavaMP3) | 1.0.1 | 4 | 4 | excluded_valid_control_crash | Mono control decodes correctly; valid 22.05 kHz stereo control crashes at `Decoder.samples_III(Decoder.java:773)`. [Probe](probes/javamp3/README.md). |
| [com.github.kokorin.jaffree:jaffree](https://central.sonatype.com/artifact/com.github.kokorin.jaffree/jaffree) | 2024.08.29 | 3 | 2 | excluded_native_wrapper | Drives an external ffprobe/ffmpeg process; parser is native FFmpeg. Not run. |
| [com.googlecode.soundlibs:basicplayer](https://central.sonatype.com/artifact/com.googlecode.soundlibs/basicplayer) | 3.0.0.0 | 0 | 0 | excluded | Player UI over mp3spi/JLayer; no parser of its own; zero direct dependents. |
| [dev.mccue:jlayer](https://central.sonatype.com/artifact/dev.mccue/jlayer) | 2024.04.19 | 0 | 0 | unresolved_shared_family | Modularized JLayer repackaging; zero deps.dev direct dependents. Same JLayer family. Not run. |
| [dev.mccue:mp3spi](https://central.sonatype.com/artifact/dev.mccue/mp3spi) | 2024.04.19 | 0 | 0 | unresolved_shared_family | Modularized MP3SPI repackaging over dev.mccue:jlayer; zero direct dependents. Same JLayer family. Not run. |
| [com.sipgate:mp3-wav](https://central.sonatype.com/artifact/com.sipgate/mp3-wav) | 1.0.4 | 0 | 0 | unresolved_no_primary_metric | MP3-to-WAV converter; zero direct dependents; decoder backend not inspected. Not run. |

Queries: `mp3`, `mp3 decoder`, `mpeg audio`, `jlayer`, `mp3spi`; limit 100 each; 112 hits, 112 unique. Maven Central ranks by text relevance and the two phrase queries returned nothing, so leads were looked up directly. See the [cell record](cell.json) for the remaining uncertainty.
