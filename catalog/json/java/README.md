# JSON / Java — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: five JSON package/API paths are control verified and runnable. jackson-databind and jackson-core share one tokenizer family; Gson, org.json and fastjson2 use independent parser engines. The com.alibaba:fastjson 2.x compatibility facade remains an unverified path in the fastjson2 family, and its summed metric also includes older 1.x releases. Eight numeric leads remain unresolved. The Maven Central search is bounded to 100 hits per query (322 unique hits); deps.dev summed direct dependents measure package adoption, not JSON-specific use. Two valid nested controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness
- [fastjson2](fastjson2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
