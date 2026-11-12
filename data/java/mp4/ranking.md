# Java × MP4: verified parser ranking

4 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T06:00:25.719625+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jcodec](https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar) | org.jcodec:jcodec:0.2.5 | 44 | track count and video dimensions | JCodec MP4 box parser |
| 2 | [isoparser](https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56-javadoc.jar) | org.mp4parser:isoparser:1.9.56 | 9 | movie track count and timescale | sannies MP4Parser ISO BMFF box parser |
| 3 | [metadata-extractor](https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0-javadoc.jar) | com.drewnoakes:metadata-extractor:2.22.0 | 6 | parsed video width and height | metadata-extractor MP4 box reader |
| 4 | [muxer](https://repo.maven.apache.org/maven2/org/mp4parser/muxer/1.9.56/muxer-1.9.56-javadoc.jar) | org.mp4parser:muxer:1.9.56 | 1 | video and audio track handlers | sannies MP4Parser movie builder over isoparser |
