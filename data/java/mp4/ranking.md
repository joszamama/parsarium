# JAVA × MP4: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev exact-version directDependentCount.

| Rank | Package | Release | Direct dependents (deps.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | 0.2.5 | 44 | track count and video dimensions | JCodec MP4 box parser |
| 2 | [old-isoparser](https://repo.maven.apache.org/maven2/com/googlecode/mp4parser/isoparser/1.1.22/isoparser-1.1.22-javadoc.jar) | 1.1.22 | 11 | movie track count and timescale | older CoreMedia/sannies MP4Parser ISO BMFF parser |
| 3 | [bytedeco-ffmpeg](https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-javadoc.jar) | 8.1.2-1.5.14 | 9 | MP4 demuxer format, two streams and video dimensions | Bytedeco binding to FFmpeg demuxer |
| 4 | [isoparser](https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56-javadoc.jar) | 1.9.56 | 9 | movie track count and timescale | sannies MP4Parser ISO BMFF box parser |
| 5 | [metadata-extractor](https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0-javadoc.jar) | 2.22.0 | 6 | parsed video width and height | metadata-extractor MP4 box reader |
| 6 | [javacv](https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14-javadoc.jar) | 1.5.14 | 4 | MP4 demuxer format, video dimensions, AAC sample rate and channels | JavaCV wrapper over FFmpeg demuxer |
| 7 | [red5-io](https://repo.maven.apache.org/maven2/org/red5/red5-io/2.0.40/red5-io-2.0.40-javadoc.jar) | 2.0.40 | 3 | MP4 video presence, parsed keyframe count and H.264/AAC codec identifiers | Red5 MP4Reader over JCodec MP4 demuxer |
| 8 | [jaffree](https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-javadoc.jar) | 2024.08.29 | 2 | MP4 H.264/AAC stream codecs, video dimensions and audio rate | Jaffree wrapper over local FFprobe/FFmpeg |
| 9 | [javasound-aac](https://repo.maven.apache.org/maven2/com/tianscar/javasound/javasound-aac/0.9.8/javasound-aac-0.9.8-javadoc.jar) | 0.9.8 | 2 | MP4 track count, AAC codec, sample rate and channels | Tianscar fork of JAAD pure Java MP4 demultiplexer |
| 10 | [jave-core](https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-javadoc.jar) | 4.2.0 | 2 | MP4 format, video dimensions, audio rate and channels | JAVE2 wrapper over bundled FFmpeg |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
