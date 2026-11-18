# JAVA × MP3: selected parsers

10 control-verified third-party paths selected from 10 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Direct dependents (deps.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | 0.2.5 | 44 | first MP3 audio frame codec, byte length and timescale from local tagged MP3 | JCodec native MPEG audio demuxer |
| 2 | [mp3spi](https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar) | 1.9.5.4 | 38 | local tagged MP3 type, ID3v2 title, artist, album and tag version | soundlibs MP3SPI Java Sound provider over its JLayer fork |
| 3 | [jlayer](https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1-javadoc.jar) | 1.0.1 | 33 | local tagged MP3 frame frequency and layer, plus ID3v2 presence | JLayer native MP3 frame decoder with raw ID3v2 access |
| 4 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | 8.1.2-1.5.14 | 9 | local tagged MP3 format, sample rate and channels | Bytedeco binding to the same FFmpeg MP3 demuxer used by JavaCV |
| 5 | [jaudiotagger](https://www.jthink.net/jaudiotagger/examples_id3.jsp) | 3.0.1 | 7 | local MP3 identification and ID3v2 title, artist and album | jaudiotagger native MP3 and ID3v2 reader |
| 6 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | 1.5.14 | 4 | local tagged MP3 format, codec, sample rate and channels | JavaCV wrapper over FFmpeg MP3 demuxer |
| 7 | [javamp3](https://github.com/delthas/JavaMP3) | 1.0.1 | 4 | 44.1 kHz tagged MP3 sample rate, channel mode and 32 decoded PCM bytes | JavaMP3 native MPEG audio decoder |
| 8 | [mp3agic](https://github.com/mpatric/mp3agic/blob/master/readme.md) | 0.9.1 | 4 | local MP3 frames and ID3v2 title, artist, album and API tag version | mp3agic native MP3 frame and ID3v2 reader |
| 9 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-sources.jar) | 2024.08.29 | 2 | local tagged MP3 codec, sample rate, title and artist | Jaffree wrapper over local FFprobe/FFmpeg |
| 10 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-sources.jar) | 4.2.0 | 2 | local tagged MP3 format, codec, sample rate and channels | JAVE2 wrapper over bundled FFmpeg MP3 demuxer |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
