# JSON / Java — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party package/API paths, 0 verified standard APIs, 3 verified Docker harnesses.

The three selected paths are jackson-databind, jackson-core, and gson. The two Jackson paths share one tokenizer family; Gson uses its own parser. The primary ranking uses deps.dev direct dependents summed over releases. Maven Central text search is relevance-ranked, and ten numeric leads remain unresolved in the bounded search. The Java SE 25 inventory found no JSON parser API. The valid nested-object and nested-array controls establish the tested behavior only.

[Ranking and search limits](../../../data/java/json/ranking.md) · [Standard API inventory](../../../data/java/json/standard.json)

## Third-party parsers

- [jackson-databind](jackson-databind/README.md) — verified Docker harness
- [jackson-core](jackson-core/README.md) — verified Docker harness
- [gson](gson/README.md) — verified Docker harness

## Standard and runtime APIs

None documented in Java SE 25.
