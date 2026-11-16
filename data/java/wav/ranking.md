# JAVA × WAV: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev exact-version directDependentCount.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | 0.2.5 | 44 | WAV sample rate, channels and bit depth | JCodec WAV demuxer |
| 2 | [metadata-extractor](https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.19.0/metadata-extractor-2.19.0-javadoc.jar) | 2.19.0 | 38 | WAV sample rate, channels and bit depth | metadata-extractor RIFF/WAV metadata reader |
| 3 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | 8.1.2-1.5.14 | 9 | WAV format, sample rate and channels | Bytedeco binding to FFmpeg demuxer |
| 4 | [jaudiotagger](https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1-javadoc.jar) | 3.0.1 | 7 | WAV header sample rate, channels and bit depth | jaudiotagger WAV reader |
| 5 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | 1.5.14 | 4 | WAV format, PCM codec, sample rate and channels | JavaCV wrapper over FFmpeg demuxer |
| 6 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | 2024.08.29 | 2 | PCM codec, sample rate and channels | Jaffree wrapper over local FFprobe/FFmpeg |
| 7 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar) | 4.2.0 | 2 | WAV format, PCM codec, sample rate and channels | JAVE2 wrapper over bundled FFmpeg |
| 8 | [jhove-modules](https://repo.maven.apache.org/maven2/org/openpreservation/jhove/jhove-modules/1.20.1/jhove-modules-1.20.1-javadoc.jar) | 1.20.1 | 1 | WAVE identification, sample rate and channels | JHOVE WAVE-hul module |
| 9 | [tika-audiovideo](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar) | 4.2.0 | 1 | WAV sample rate and channels in parsed metadata | Apache Tika AudioParser over Java Sound SPI |
| 10 | [wavfile](https://repo.maven.apache.org/maven2/com/github/psambit9791/wavfile/1.0.0/wavfile-1.0.0-javadoc.jar) | 1.0.0 | 1 | sample rate, channels, frame count and four PCM samples | wavfile Java WAV reader |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
