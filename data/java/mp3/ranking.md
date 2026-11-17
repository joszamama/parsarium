# JAVA × MP3: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-adoption lead whose own Java code parses untagged MPEG Layer III frames, and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

The selected path, [jcodec](../../../projects/mp3/java/jcodec/README.md) 0.2.5, synchronizes every frame with `MPEGAudioDemuxer` and decodes each one with its pure-Java `Mp3Decoder`. It is the same JCodec package and demuxer already counted in the active Java MP3-with-ID3v2 cell, so it is a separate plain-frame path in the same parser family, not an independent family.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). The single-release maximum is recorded as a cross-check. The count covers the whole jcodec library, not MP3 use alone.

| Rank | Package | Release | Metric | Max single release | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [org.jcodec:jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | 0.2.5 | 76 | 44 (0.2.5) | Every frame of an untagged stream: codec, sample rate, channels, frames, decoded samples | JCodec native MPEG audio demuxer |

Controls: `controls/mp3/tone-44k-mono.mp3` gives MP3, 44,100 Hz, 1 channel, 11 frames, 12,672 samples; the AFL++ differential `controls/mp3/tone-22k-stereo.mp3` gives 22,050 Hz, 2 channels, 12 frames, 6,912 samples. Both match the libmpg123 pilot. JaCoCo covers 1,142 jcodec source lines on the primary control. Repeated AFL++ probes are identical and the stereo control changes 185 AFL++ tuples ([feedback receipt](afl-feedback.json)).

javacv (315) and org.bytedeco:ffmpeg (215) have higher counts but are JNI wrappers: MP3 parsing runs in native FFmpeg, with no Java parser source to cover. They are excluded here, not ranked.

## Standard API (none)

OpenJDK 25.0.5 Java Sound has readers for WAV, AU and AIFF only; `AudioSystem.getAudioFileFormat` and `getAudioInputStream` throw `UnsupportedAudioFileException` on the primary control. Details in [standard.json](standard.json).

## Lead log

Looked up on deps.dev; none is a verified entry.

| Lead | Version seen | Summed direct dependents | Max single release | Status | Note |
| --- | --- | ---: | ---: | --- | --- |
| [org.bytedeco:javacv](https://central.sonatype.com/artifact/org.bytedeco/javacv) | 1.5.14 | 315 | 69 | excluded_native_wrapper | FFmpegFrameGrabber is a JNI wrapper; MP3 frame parsing and decoding run in native FFmpeg (libavformat/libavcodec), so there are no Java parser source lines for JaCoCo. The C/FFmpeg family belongs to a native cell. Recorded as FFmpeg family in data/java/mp3_id3v2/parsers.json. |
| [org.bytedeco:ffmpeg](https://central.sonatype.com/artifact/org.bytedeco/ffmpeg) | 8.1.2-1.5.14 | 215 | 76 | excluded_native_wrapper | JavaCPP binding to the same native FFmpeg demuxer and decoder as javacv; no Java parser source. Not run. |
| [com.googlecode.soundlibs:mp3spi](https://central.sonatype.com/artifact/com.googlecode.soundlibs/mp3spi) | 1.9.5.4 | 55 | 38 | unresolved | Java Sound SPI (MpegAudioFileReader) over the soundlibs JLayer fork, a pure-Java Layer III decoder; next-highest Java parser lead (55). Control not run in this pilot. Same JLayer lineage as javazoom:jlayer. |
| [ws.schild:jave-core](https://central.sonatype.com/artifact/ws.schild/jave-core) | 4.2.0 | 52 | 9 | excluded_native_wrapper | Runs a bundled ffmpeg executable and parses its text output; parser is native FFmpeg. Not run. |
| [javazoom:jlayer](https://central.sonatype.com/artifact/javazoom/jlayer) | 1.0.1 | 33 | 33 | unresolved | Bitstream.readFrame()/Decoder.decodeFrame over InputStream, pure-Java Layer III decoder. Control not run in this pilot. |
| [com.badlogicgames.jlayer:jlayer](https://central.sonatype.com/artifact/com.badlogicgames.jlayer/jlayer) | 1.0.2-gdx | 30 | 26 | unresolved_shared_family | libGDX repackaging of JLayer; same decoder family as javazoom:jlayer. Not run. |
| [com.googlecode.soundlibs:jlayer](https://central.sonatype.com/artifact/com.googlecode.soundlibs/jlayer) | 1.0.1.4 | 28 | 14 | unresolved_shared_family | Maintained fork of javazoom JLayer; same decoder family as javazoom:jlayer. Not run. |
| [com.soywiz:korau-mp3](https://central.sonatype.com/artifact/com.soywiz/korau-mp3) | 0.19.1 | 25 | 2 | unresolved | Kotlin korau MP3 decoder module published to Maven (last release 0.19.1); decoder lineage not inspected. Control not run. |
| [net.jthink:jaudiotagger](https://central.sonatype.com/artifact/net.jthink/jaudiotagger) | 3.0.1 | 8 | 7 | unresolved | MP3AudioHeader scans MPEG frame headers (bitrate, sample rate, channel mode, frame count) but does not decode; tag library first. Control not run. |
| [com.mpatric:mp3agic](https://central.sonatype.com/artifact/com.mpatric/mp3agic) | 0.9.1 | 6 | 4 | unresolved | new Mp3File(Path) scans MPEG frame headers for bitrate, sample rate and channel mode; no decode. Control not run. |
| [fr.delthas:javamp3](https://central.sonatype.com/artifact/fr.delthas/javamp3) | 1.0.1 | 4 | 4 | unresolved | Sound(InputStream) pure-Java Layer III decoder. Control not run. |
| [com.github.kokorin.jaffree:jaffree](https://central.sonatype.com/artifact/com.github.kokorin.jaffree/jaffree) | 2024.08.29 | 3 | 2 | excluded_native_wrapper | Drives an external ffprobe/ffmpeg process; parser is native FFmpeg. Not run. |
| [com.googlecode.soundlibs:basicplayer](https://central.sonatype.com/artifact/com.googlecode.soundlibs/basicplayer) | 3.0.0.0 | 0 | 0 | excluded | Player UI over mp3spi/JLayer; no parser of its own; zero direct dependents. |
| [dev.mccue:jlayer](https://central.sonatype.com/artifact/dev.mccue/jlayer) | 2024.04.19 | 0 | 0 | unresolved_shared_family | Modularized JLayer repackaging; zero deps.dev direct dependents. Same JLayer family. Not run. |
| [dev.mccue:mp3spi](https://central.sonatype.com/artifact/dev.mccue/mp3spi) | 2024.04.19 | 0 | 0 | unresolved_shared_family | Modularized MP3SPI repackaging over dev.mccue:jlayer; zero direct dependents. Same JLayer family. Not run. |
| [com.sipgate:mp3-wav](https://central.sonatype.com/artifact/com.sipgate/mp3-wav) | 1.0.4 | 0 | 0 | unresolved_no_primary_metric | MP3-to-WAV converter; zero direct dependents; decoder backend not inspected. Not run. |

Queries: `mp3`, `mp3 decoder`, `mpeg audio`, `jlayer`, `mp3spi`; limit 100 each; 112 hits, 112 unique. Maven Central ranks by text relevance and the two phrase queries returned nothing, so leads were looked up directly. See the [cell record](cell.json) for the remaining uncertainty.
