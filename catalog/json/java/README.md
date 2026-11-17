# JSON / Java — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: the two highest-adoption general-purpose JSON parser leads from independent parser families were built and control-verified: jackson-databind (162,890 deps.dev direct dependents summed over 239 releases) and gson (33,240 over 45 releases). jackson-core, the second-highest lead (80,053), is the tokenizer jackson-databind drives, so it stays a same-family lead rather than a separate path. Maven Central text search ranks by relevance, not adoption, so leads were looked up directly on deps.dev; the remaining eleven are logged in leads.json and are not selected or ranked. The Jackson adapter disables CANONICALIZE_FIELD_NAMES for deterministic feedback; Gson uses its default instance. Java SE 25 exports no JSON parsing API, so the standard count is zero by inventory, not by omission. Valid nested object and nested array controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
