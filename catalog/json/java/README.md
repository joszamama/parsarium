# JSON / Java — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four selected JSON package/API paths have pinned valid-control containers and parser-derived AFL++ feedback. jackson-databind and jackson-core share the Jackson tokenizer; Gson and fastjson2 have independent engines. Nine numeric leads remain unresolved in the bounded search of 322 unique hits. The deps.dev metric measures package adoption, not JSON-specific use. Valid nested controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness
- [fastjson2](fastjson2/README.md) — verified Docker harness

## Standard and runtime APIs

None documented in Java SE 25.
