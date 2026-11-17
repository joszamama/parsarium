# Java × SQL: pilot ranking

Six third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

deps.dev directDependentCount summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [org.jooq:jooq](https://www.jooq.org/doc/3.21/manual/sql-building/sql-parser/sql-parser-api/) | 3.21.9 | 4,574 | `DSL.using(SQLDialect.DEFAULT).parser().parse(local SQL text) -> Queries`; dialect: SQLDialect.DEFAULT | jOOQ hand-written recursive-descent parser (ParserImpl) and query object model |
| 2 | [com.alibaba:druid](https://github.com/alibaba/druid/wiki/SQL-Parser) | 1.2.28 | 1,945 | `SQLUtils.parseStatements(local SQL text, DbType.mysql) -> List<SQLStatement>`; dialect: DbType.mysql | Druid hand-written SQL lexer and recursive-descent parsers |
| 3 | [com.facebook.presto:presto-parser](https://javadoc.io/doc/com.facebook.presto/presto-parser/0.300/com/facebook/presto/sql/parser/SqlParser.html) | 0.300 | 1,453 | `SqlParser.createStatement(statement text from StatementSplitter over local SQL text, ParsingOptions with DecimalLiteralTreatment.AS_DECIMAL) -> Statement`; dialect: Presto SQL (the only grammar; ParsingOptions DecimalLiteralTreatment.AS_DECIMAL so 19.5 is a DecimalLiteral) | Presto/Trino ANTLR4 SqlBase grammar (Presto branch) |
| 4 | [org.apache.calcite:calcite-core](https://calcite.apache.org/javadocAggregate/org/apache/calcite/sql/parser/SqlParser.html) | 1.42.0 | 1,250 | `SqlParser.create(local SQL text, SqlParser.config()).parseStmtList() -> SqlNodeList`; dialect: SqlParser.config() default (Calcite default lexical policy and SqlConformanceEnum.DEFAULT) | Apache Calcite JavaCC grammar (SqlParserImpl) |
| 5 | [com.github.jsqlparser:jsqlparser](https://jsqlparser.github.io/JSqlParser/usage.html) | 5.4 | 950 | `CCJSqlParserUtil.parseStatements(local SQL text) -> Statements`; dialect: JSqlParser default parser features (no dialect switch; CCJSqlParserUtil.parseStatements without a parser consumer) | JSqlParser JavaCC grammar (CCJSqlParser) |
| 6 | [io.trino:trino-parser](https://javadoc.io/doc/io.trino/trino-parser/484/io/trino/sql/parser/SqlParser.html) | 484 | 525 | `new SqlParser().createStatement(local SQL text without its terminating semicolon) -> Statement`; dialect: Trino SQL (the only grammar; no parsing options) | Presto/Trino ANTLR4 SqlBase grammar (Trino branch) |

Receipts: [org.jooq:jooq](../../../projects/sql/java/jooq/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/jooq/differential.json), [com.alibaba:druid](../../../projects/sql/java/druid/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/druid/differential.json), [com.facebook.presto:presto-parser](../../../projects/sql/java/presto_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/presto_parser/differential.json), [org.apache.calcite:calcite-core](../../../projects/sql/java/calcite/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/calcite/differential.json), [com.github.jsqlparser:jsqlparser](../../../projects/sql/java/jsqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/jsqlparser/differential.json) and [io.trino:trino-parser](../../../projects/sql/java/trino_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/trino_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| org.jooq:jooq | 4,574 | selected | jOOQ hand-written parser |
| com.alibaba:druid | 1,945 | selected | Druid hand-written SQL parser |
| com.facebook.presto:presto-parser | 1,453 | selected | Presto/Trino ANTLR grammar |
| org.apache.calcite:calcite-core | 1,250 | selected | Calcite JavaCC grammar |
| com.github.jsqlparser:jsqlparser | 950 | selected | JSqlParser JavaCC grammar |
| io.trino:trino-parser | 525 | selected | Presto/Trino ANTLR grammar |
| io.prestosql:presto-parser | 282 | unresolved | Presto/Trino ANTLR grammar |
| org.apache.spark:spark-catalyst_2.13 | 278 | unresolved | Spark SQL ANTLR grammar |
| org.apache.shardingsphere:shardingsphere-sql-parser-engine | 135 | unresolved | ShardingSphere ANTLR grammars |
| com.github.vertical-blank:sql-formatter | 111 | excluded | — |
| net.sf.jsqlparser:jsqlparser | 8 | excluded | JSqlParser JavaCC grammar |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
