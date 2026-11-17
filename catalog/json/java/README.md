# JSON / Java — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: four high-adoption JSON package/API paths are control verified and runnable. jackson-databind and jackson-core share one tokenizer family; Gson and fastjson2 have independent parser engines. The com.alibaba:fastjson 2.x compatibility facade remains a lead in the fastjson2 family, not a separate verified engine. Nine numeric leads remain unresolved. The Maven Central search is bounded to 100 hits per query (322 unique hits); deps.dev summed direct dependents measure package adoption, not JSON-specific use. Valid nested-object and nested-array controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness
- [fastjson2](fastjson2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
