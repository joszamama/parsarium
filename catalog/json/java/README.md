# JSON / Java — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Pilot cell: ten JSON package/API paths are control-verified and runnable. Jackson databind and core share a tokenizer family; Gson, fastjson 1.x, org.json, fastjson2, json-simple, json-smart, Moshi, and Parsson are separate parser families. Fastjson 1.2.83 has its own DefaultJSONParser/JSONLexer; the com.alibaba:fastjson coordinate adoption metric sums both 1.x and later 2.x fastjson2 facade releases, so it is not a 1.x-only count. Its pinned-release direct-dependent count is separately recorded. Json-simple 1.1.1 is an older 2012 release with a high default-release count, so ranking uses the common deps.dev summed metric. Json-smart is verified on its RFC 4627 object/array mode, not scalar roots. Parsson implements Jakarta JSON-P with its own tokenizer over a local InputStream; the Jakarta API jar supplies interfaces. Three numeric leads remain unverified. Maven Central search is bounded to 100 hits per query (322 unique hits); deps.dev counts measure package adoption, not JSON-specific use. Two valid nested controls do not establish complete format coverage.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness · [source repository](<https://github.com/FasterXML/jackson-databind>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.jackson.core/jackson-databind>)
- [jackson-core](jackson-core/README.md) — verified Docker harness · [source repository](<https://github.com/FasterXML/jackson-core>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.jackson.core/jackson-core>)
- [gson](gson/README.md) — verified Docker harness · [source repository](<https://github.com/google/gson>) · [Maven Central](<https://central.sonatype.com/artifact/com.google.code.gson/gson>)
- [fastjson](fastjson/README.md) — verified Docker harness · [source repository](<https://github.com/alibaba/fastjson>) · [Maven Central](<https://central.sonatype.com/artifact/com.alibaba/fastjson>)
- [json](json/README.md) — verified Docker harness · [source repository](<https://github.com/stleary/JSON-java>) · [Maven Central](<https://central.sonatype.com/artifact/org.json/json>)
- [fastjson2](fastjson2/README.md) — verified Docker harness · [source repository](<https://github.com/alibaba/fastjson2>) · [Maven Central](<https://central.sonatype.com/artifact/com.alibaba.fastjson2/fastjson2>)
- [json-simple](json-simple/README.md) — verified Docker harness · [Maven Central](<https://central.sonatype.com/artifact/com.googlecode.json-simple/json-simple>)
- [json-smart](json-smart/README.md) — verified Docker harness · [source repository](<https://github.com/netplex/json-smart-v2>) · [Maven Central](<https://central.sonatype.com/artifact/net.minidev/json-smart>)
- [moshi](moshi/README.md) — verified Docker harness · [source repository](<https://github.com/square/moshi>) · [Maven Central](<https://central.sonatype.com/artifact/com.squareup.moshi/moshi>)
- [parsson](parsson/README.md) — verified Docker harness · [source repository](<https://github.com/eclipse-ee4j/parsson>) · [Maven Central](<https://central.sonatype.com/artifact/org.eclipse.parsson/parsson>)

## Standard and runtime APIs

None verified in this pilot cell yet.
