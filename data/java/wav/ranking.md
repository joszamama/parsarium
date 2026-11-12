# Java × WAV: verified parser ranking

9 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T05:11:29.289209+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | org.jcodec:jcodec:0.2.5 | 44 | WAV sample rate, channels and bit depth | JCodec WAV demuxer |
| 2 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | org.bytedeco:ffmpeg:8.1.2-1.5.14 | 9 | WAV format, sample rate and channels | Bytedeco binding to FFmpeg demuxer |
| 3 | [jaudiotagger](https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1-javadoc.jar) | net.jthink:jaudiotagger:3.0.1 | 7 | WAV header sample rate, channels and bit depth | jaudiotagger WAV reader |
| 4 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | org.bytedeco:javacv:1.5.14 | 4 | WAV format, PCM codec, sample rate and channels | JavaCV wrapper over FFmpeg demuxer |
| 5 | [tika-audiovideo](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar) | org.apache.tika:tika-parser-audiovideo-module:4.2.0 | 1 | WAV sample rate and channels in parsed metadata | Apache Tika AudioParser over Java Sound SPI |
| 5 | [wavfile](https://repo.maven.apache.org/maven2/com/github/psambit9791/wavfile/1.0.0/wavfile-1.0.0-javadoc.jar) | com.github.psambit9791:wavfile:1.0.0 | 1 | sample rate, channels, frame count and four PCM samples | wavfile Java WAV reader |
| 7 | [beads](https://repo.maven.apache.org/maven2/net/beadsproject/beads/3.2/beads-3.2-javadoc.jar) | net.beadsproject:beads:3.2 | 0 | sample rate, channels and decoded frame count | Beads WAV reader |
| 7 | [codecmedia](https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2-javadoc.jar) | me.tamkungz.codecmedia:codecmedia:1.2.2 | 0 | parsed PCM codec, sample rate and channels | CodecMedia RIFF/WAV parser |
| 7 | [jdsp](https://repo.maven.apache.org/maven2/com/github/psambit9791/jdsp/3.1.1/jdsp-3.1.1-javadoc.jar) | com.github.psambit9791:jdsp:3.1.1 | 0 | sample rate, channels and frame count | JDSP WAV API over wavfile |
