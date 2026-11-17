# JSON / Java — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Nine JSON package/API paths are control-verified and runnable. jackson-databind and jackson-core share one tokenizer family. Gson, org.json, fastjson 1.x, fastjson2, json-simple, json-smart, and Moshi use independent engines. fastjson 1.2.83 was selected as the independent 1.x engine; its package-coordinate metric also includes 2.x facade releases over fastjson2 and cannot measure 1.x alone. Four numeric leads remain unresolved. Maven Central search is bounded to 100 hits per query (322 unique hits); deps.dev summed direct dependents measure package adoption, not JSON-specific use. Two valid nested controls do not establish complete format coverage.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness
- [fastjson](fastjson/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness
- [fastjson2](fastjson2/README.md) — verified Docker harness
- [json-simple](json-simple/README.md) — verified Docker harness
- [json-smart](json-smart/README.md) — verified Docker harness
- [moshi](moshi/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
