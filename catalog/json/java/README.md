# JSON / Java — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: only the highest-adoption general-purpose JSON parser lead (jackson-databind, 162,890 deps.dev direct dependents summed over 239 releases) was built and control-verified. Maven Central text search ranks by relevance, not adoption, so twelve leads were looked up directly on deps.dev and are logged in leads.json; they are not selected or ranked. The adapter disables CANONICALIZE_FIELD_NAMES for deterministic feedback. Java SE 25 exports no JSON parsing API, so the standard count is zero by inventory, not by omission. One valid nested object control does not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
