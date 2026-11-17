# JSON / Java — pilot

**Status:** pilot_seven_selected_search_bounded; incomplete. 7 verified third-party paths, 0 verified standard APIs, 7 verified Docker harnesses.

Pilot cell: seven JSON package/API paths are control verified and runnable. jackson-databind and jackson-core share one tokenizer family; Gson, org.json, fastjson2, json-smart, and Moshi use independent parser engines. json-smart is verified on its RFC 4627 object/array mode, not scalar roots. Moshi reads local bytes through Okio and its own JsonUtf8Reader. The com.alibaba:fastjson 2.x compatibility facade remains an unverified path in the fastjson2 family, and its summed metric also includes older 1.x releases. Six numeric leads remain unresolved, including higher-metric json-simple. The Maven Central search is bounded to 100 hits per query (322 unique hits); deps.dev summed direct dependents measure package adoption, not JSON-specific use. Two valid nested controls do not establish complete format coverage.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness
- [fastjson2](fastjson2/README.md) — verified Docker harness
- [json-smart](json-smart/README.md) — verified Docker harness
- [moshi](moshi/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
