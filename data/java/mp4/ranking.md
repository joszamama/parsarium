# Java × MP4: verified parser ranking

12 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T06:15:58.295059+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | org.jcodec:jcodec:0.2.5 | 44 | track count and video dimensions | JCodec MP4 box parser |
| 2 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | org.bytedeco:ffmpeg:8.1.2-1.5.14 | 9 | MP4 demuxer format, two streams and video dimensions | Bytedeco binding to FFmpeg demuxer |
| 2 | [isoparser](https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56-javadoc.jar) | org.mp4parser:isoparser:1.9.56 | 9 | movie track count and timescale | sannies MP4Parser ISO BMFF box parser |
| 4 | [metadata-extractor](https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0-javadoc.jar) | com.drewnoakes:metadata-extractor:2.22.0 | 6 | parsed video width and height | metadata-extractor MP4 box reader |
| 5 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | org.bytedeco:javacv:1.5.14 | 4 | MP4 demuxer format, video dimensions, AAC sample rate and channels | JavaCV wrapper over FFmpeg demuxer |
| 6 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | com.github.kokorin.jaffree:jaffree:2024.08.29 | 2 | MP4 H.264/AAC stream codecs, video dimensions and audio rate | Jaffree wrapper over local FFprobe/FFmpeg |
| 6 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar) | ws.schild:jave-core:4.2.0 | 2 | MP4 format, video dimensions, audio rate and channels | JAVE2 wrapper over bundled FFmpeg |
| 8 | [muxer](https://repo.maven.apache.org/maven2/org/mp4parser/muxer/1.9.56/muxer-1.9.56-javadoc.jar) | org.mp4parser:muxer:1.9.56 | 1 | video and audio track handlers | sannies MP4Parser movie builder over isoparser |
| 8 | [tika-mp4](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar) | org.apache.tika:tika-parser-audiovideo-module:4.2.0 | 1 | parsed video dimensions, audio properties and title | Apache Tika MP4Parser over metadata-extractor |
| 10 | [bramp-ffmpeg](https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar) | net.bramp.ffmpeg:ffmpeg:0.9.2 | 0 | MP4 demuxer format, H.264/AAC stream codecs, video dimensions and audio rate | bramp FFprobe CLI wrapper over FFmpeg |
| 10 | [imagic-ffmpeg-java](https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2-javadoc.jar) | ch.imagic:ffmpeg-java:0.1.2 | 0 | MP4 demuxer format, H.264/AAC stream codecs, video dimensions and audio rate | Imagic fork of bramp FFprobe CLI wrapper over FFmpeg |
| 10 | [v47-jaffree](https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-javadoc.jar) | io.v47.jaffree:jaffree:2.1.0 | 0 | MP4 H.264/AAC stream codecs, video dimensions and audio rate | v47 fork of Jaffree FFprobe CLI wrapper over FFmpeg |
