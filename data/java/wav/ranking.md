# Java × WAV: verified parser ranking

17 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T05:40:19.373367+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 1 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | org.jcodec:jcodec:0.2.5 | 44 | WAV sample rate, channels and bit depth | JCodec WAV demuxer |
| 2 | [metadata-extractor](https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.19.0/metadata-extractor-2.19.0-javadoc.jar) | com.drewnoakes:metadata-extractor:2.19.0 | 38 | WAV sample rate, channels and bit depth | metadata-extractor RIFF/WAV metadata reader |
| 3 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | org.bytedeco:ffmpeg:8.1.2-1.5.14 | 9 | WAV format, sample rate and channels | Bytedeco binding to FFmpeg demuxer |
| 4 | [jaudiotagger](https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1-javadoc.jar) | net.jthink:jaudiotagger:3.0.1 | 7 | WAV header sample rate, channels and bit depth | jaudiotagger WAV reader |
| 5 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | org.bytedeco:javacv:1.5.14 | 4 | WAV format, PCM codec, sample rate and channels | JavaCV wrapper over FFmpeg demuxer |
| 6 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | com.github.kokorin.jaffree:jaffree:2024.08.29 | 2 | PCM codec, sample rate and channels | Jaffree wrapper over local FFprobe/FFmpeg |
| 6 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar) | ws.schild:jave-core:4.2.0 | 2 | WAV format, PCM codec, sample rate and channels | JAVE2 wrapper over bundled FFmpeg |
| 8 | [jhove-modules](https://repo.maven.apache.org/maven2/org/openpreservation/jhove/jhove-modules/1.20.1/jhove-modules-1.20.1-javadoc.jar) | org.openpreservation.jhove:jhove-modules:1.20.1 | 1 | WAVE identification, sample rate and channels | JHOVE WAVE-hul module |
| 8 | [tika-audiovideo](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar) | org.apache.tika:tika-parser-audiovideo-module:4.2.0 | 1 | WAV sample rate and channels in parsed metadata | Apache Tika AudioParser over Java Sound SPI |
| 8 | [wavfile](https://repo.maven.apache.org/maven2/com/github/psambit9791/wavfile/1.0.0/wavfile-1.0.0-javadoc.jar) | com.github.psambit9791:wavfile:1.0.0 | 1 | sample rate, channels, frame count and four PCM samples | wavfile Java WAV reader |
| 11 | [beads](https://repo.maven.apache.org/maven2/net/beadsproject/beads/3.2/beads-3.2-javadoc.jar) | net.beadsproject:beads:3.2 | 0 | sample rate, channels and decoded frame count | Beads WAV reader |
| 11 | [bramp-ffmpeg](https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar) | net.bramp.ffmpeg:ffmpeg:0.9.2 | 0 | WAV format, PCM codec, sample rate and channels | bramp FFprobe CLI wrapper over FFmpeg |
| 11 | [codecmedia](https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2-javadoc.jar) | me.tamkungz.codecmedia:codecmedia:1.2.2 | 0 | parsed PCM codec, sample rate and channels | CodecMedia RIFF/WAV parser |
| 11 | [imagic-ffmpeg-java](https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar) | ch.imagic:ffmpeg-java:0.1.2 | 0 | WAV format, PCM codec, sample rate and channels | Imagic fork of bramp FFprobe CLI wrapper over FFmpeg |
| 11 | [jdsp](https://repo.maven.apache.org/maven2/com/github/psambit9791/jdsp/3.1.1/jdsp-3.1.1-javadoc.jar) | com.github.psambit9791:jdsp:3.1.1 | 0 | sample rate, channels and frame count | JDSP WAV API over wavfile |
| 11 | [musicg](https://repo.maven.apache.org/maven2/com/github/fracpete/musicg/1.4.2.2/musicg-1.4.2.2-javadoc.jar) | com.github.fracpete:musicg:1.4.2.2 | 0 | WAVE format, sample rate, channels, bit depth and sample count | musicg PCM WAVE reader |
| unranked | [tarsosdsp-jvm](https://mvn.0110.be/releases/be/tarsos/dsp/jvm/2.5/jvm-2.5-javadoc.jar) | be.tarsos.dsp:jvm:2.5 | unknown | sample rate, channels, bit depth and decoded frame count | TarsosDSP JVM wrapper over Java Sound |
