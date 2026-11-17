# Java × SQL: pilot ranking

One third-party path is control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

deps.dev directDependentCount summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [org.jooq:jooq](https://www.jooq.org/doc/3.21/manual/sql-building/sql-parser/sql-parser-api/) | 3.21.9 | 4,574 | `DSL.using(SQLDialect.DEFAULT).parser().parse(local SQL text) -> Queries`; dialect: SQLDialect.DEFAULT | jOOQ hand-written recursive-descent parser (ParserImpl) and query object model |

Receipts: [org.jooq:jooq](../../../projects/sql/java/jooq/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/jooq/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| org.jooq:jooq | 4,574 | selected | jOOQ hand-written parser |
| com.alibaba:druid | 1,945 | unresolved | Druid hand-written SQL parser |
| com.facebook.presto:presto-parser | 1,453 | unresolved | Presto/Trino ANTLR grammar |
| org.apache.calcite:calcite-core | 1,250 | unresolved | Calcite JavaCC grammar |
| com.github.jsqlparser:jsqlparser | 950 | unresolved | JSqlParser JavaCC grammar |
| io.trino:trino-parser | 525 | unresolved | Presto/Trino ANTLR grammar |
| io.prestosql:presto-parser | 282 | unresolved | Presto/Trino ANTLR grammar |
| org.apache.spark:spark-catalyst_2.13 | 278 | unresolved | Spark SQL ANTLR grammar |
| org.apache.shardingsphere:shardingsphere-sql-parser-engine | 135 | unresolved | ShardingSphere ANTLR grammars |
| com.github.vertical-blank:sql-formatter | 111 | excluded | — |
| net.sf.jsqlparser:jsqlparser | 8 | excluded | JSqlParser JavaCC grammar |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
