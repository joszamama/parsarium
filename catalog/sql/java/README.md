# SQL / Java — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified Java SQL paths after a bounded Maven Central search (three queries, 143 hits) and deps.dev direct dependents summed over releases for 11 targeted leads, captured 2026-11-17. org.jooq:jooq 3.21.9 (4,574) and com.alibaba:druid 1.2.28 (1,945) parse both valid controls into their own ASTs, which give the oracle summary. Both metrics mostly count other uses: jOOQ's query builder and Druid's JDBC connection pool, which ship in the same jars. presto-parser, Calcite, JSqlParser, Trino and other leads are unverified, so this is not a top-ten ranking. java.sql has no SQL parser. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/java/sql/ranking.md) · [Standard API inventory](../../../data/java/sql/standard.json)

## Third-party parsers

- [org.jooq:jooq](org-jooq-jooq/README.md) — verified Docker harness
- [com.alibaba:druid](com-alibaba-druid/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
