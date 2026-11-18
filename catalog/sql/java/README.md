# SQL / Java — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten verified Java SQL paths, the ceiling, after a bounded Maven Central search (three queries, 143 hits) and deps.dev direct dependents summed over releases for 11 targeted leads, captured 2026-11-17, plus 14 more coordinates measured by the same function (Hive, Flink, Spark, ShardingSphere renames, ZetaSQL, Calcite Babel and others). org.jooq:jooq 3.21.9 (4,574), com.alibaba:druid 1.2.28 (1,945), com.facebook.presto:presto-parser 0.300 (1,453), org.apache.calcite:calcite-core 1.42.0 (1,250), org.apache.hive:hive-exec 4.2.1 (1,146), com.github.jsqlparser:jsqlparser 5.4 (950), org.apache.spark:spark-catalyst_2.12 3.5.9 (529), io.trino:trino-parser 484 (525), org.apache.flink:flink-sql-parser 2.3.0 (188) and org.apache.shardingsphere:shardingsphere-sql-parser-engine 5.3.2 (135) parse both valid controls into their own trees, which give the oracle summary. The metrics mostly count other uses for jOOQ (query builder), Druid (JDBC connection pool), Calcite (planner and adapters), hive-exec (Hive's execution engine) and spark-catalyst (Spark SQL's analyzer and optimizer), and every value is summed over releases. Two families have two paths: presto-parser and trino-parser share the Presto/Trino SqlBase grammar ancestry, and flink-sql-parser generates its own parser from Calcite's grammar template on top of calcite-core 1.36; each pair is a separate package with its own generated parser. trino-parser and hive-exec have no public statement splitter, so their adapters remove the terminating semicolon; trino-parser, hive-exec, spark-catalyst and ShardingSphere parse one statement, so statement_count is 1 by API contract. Spark's catalyst API is published but marked internal, and its parser rewrites COUNT(*) to count(1), whose synthesized literal is excluded by its origin span. Hive's coverage sources are regenerated with ANTLR 3.5.2 from the pinned grammars and checked against the shipped line tables. ShardingSphere is pinned at the last release of its documented pre-5.4 coordinates; the renamed successor coordinates are not added. The Calcite, Hive, Spark, Flink and ShardingSphere paths pin only the jars their parser paths load. org.apache.spark:spark-sql_2.12 (3,567), Spark's engine module whose internal SparkSqlParser extends the selected catalyst AstBuilder, stays an unrun lead: it would be a same-family wrapper with no own differential on these controls. io.prestosql:presto-parser is excluded as Trino's predecessor name and the ShardingSphere 5.4+ coordinates as renames. Ten paths do not establish a definitive most-used ten. java.sql has no SQL parser. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/java/sql/ranking.md) · [Standard API inventory](../../../data/java/sql/standard.json)

## Third-party parsers

- [org.jooq:jooq](org-jooq-jooq/README.md) — verified Docker harness
- [com.alibaba:druid](com-alibaba-druid/README.md) — verified Docker harness
- [com.facebook.presto:presto-parser](com-facebook-presto-presto-parser/README.md) — verified Docker harness
- [org.apache.calcite:calcite-core](org-apache-calcite-calcite-core/README.md) — verified Docker harness
- [org.apache.hive:hive-exec](org-apache-hive-hive-exec/README.md) — verified Docker harness
- [com.github.jsqlparser:jsqlparser](com-github-jsqlparser-jsqlparser/README.md) — verified Docker harness
- [org.apache.spark:spark-catalyst_2.12](org-apache-spark-spark-catalyst-2-12/README.md) — verified Docker harness
- [io.trino:trino-parser](io-trino-trino-parser/README.md) — verified Docker harness
- [org.apache.flink:flink-sql-parser](org-apache-flink-flink-sql-parser/README.md) — verified Docker harness
- [org.apache.shardingsphere:shardingsphere-sql-parser-engine](org-apache-shardingsphere-shardingsphere-sql-parser-engine/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
