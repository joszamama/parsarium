# Java × MP3 with ID3v2: verified parser ranking

9 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T14:25:32.356413+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mp3spi](https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar) | com.googlecode.soundlibs:mp3spi:1.9.5.4 | 38 | local tagged MP3 type, ID3v2 title, artist, album and tag version | soundlibs MP3SPI Java Sound provider over its JLayer fork |
| 2 | [jlayer](https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1-javadoc.jar) | javazoom:jlayer:1.0.1 | 33 | local tagged MP3 frame frequency and layer, plus ID3v2 presence | JLayer native MP3 frame decoder with raw ID3v2 access |
| 3 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | org.bytedeco:ffmpeg:8.1.2-1.5.14 | 9 | local tagged MP3 format, sample rate and channels | Bytedeco binding to the same FFmpeg MP3 demuxer used by JavaCV |
| 4 | [jaudiotagger](https://www.jthink.net/jaudiotagger/examples_id3.jsp) | net.jthink:jaudiotagger:3.0.1 | 7 | local MP3 identification and ID3v2 title, artist and album | jaudiotagger native MP3 and ID3v2 reader |
| 5 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | org.bytedeco:javacv:1.5.14 | 4 | local tagged MP3 format, codec, sample rate and channels | JavaCV wrapper over FFmpeg MP3 demuxer |
| 5 | [mp3agic](https://github.com/mpatric/mp3agic/blob/master/readme.md) | com.mpatric:mp3agic:0.9.1 | 4 | local MP3 frames and ID3v2 title, artist, album and API tag version | mp3agic native MP3 frame and ID3v2 reader |
| 7 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-sources.jar) | com.github.kokorin.jaffree:jaffree:2024.08.29 | 2 | local tagged MP3 codec, sample rate, title and artist | Jaffree wrapper over local FFprobe/FFmpeg |
| 7 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-sources.jar) | ws.schild:jave-core:4.2.0 | 2 | local tagged MP3 format, codec, sample rate and channels | JAVE2 wrapper over bundled FFmpeg MP3 demuxer |
| 9 | [tika-audiovideo](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-sources.jar) | org.apache.tika:tika-parser-audiovideo-module:4.2.0 | 1 | local tagged MP3 title, artist and album metadata | Apache Tika native MP3 and ID3v2 parser |
