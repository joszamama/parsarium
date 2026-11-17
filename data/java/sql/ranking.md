# Java × SQL: pilot ranking

Ten third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

deps.dev directDependentCount summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [org.jooq:jooq](https://www.jooq.org/doc/3.21/manual/sql-building/sql-parser/sql-parser-api/) | 3.21.9 | 4,574 | `DSL.using(SQLDialect.DEFAULT).parser().parse(local SQL text) -> Queries`; dialect: SQLDialect.DEFAULT | jOOQ hand-written recursive-descent parser (ParserImpl) and query object model |
| 2 | [com.alibaba:druid](https://github.com/alibaba/druid/wiki/SQL-Parser) | 1.2.28 | 1,945 | `SQLUtils.parseStatements(local SQL text, DbType.mysql) -> List<SQLStatement>`; dialect: DbType.mysql | Druid hand-written SQL lexer and recursive-descent parsers |
| 3 | [com.facebook.presto:presto-parser](https://javadoc.io/doc/com.facebook.presto/presto-parser/0.300/com/facebook/presto/sql/parser/SqlParser.html) | 0.300 | 1,453 | `SqlParser.createStatement(statement text from StatementSplitter over local SQL text, ParsingOptions with DecimalLiteralTreatment.AS_DECIMAL) -> Statement`; dialect: Presto SQL (the only grammar; ParsingOptions DecimalLiteralTreatment.AS_DECIMAL so 19.5 is a DecimalLiteral) | Presto/Trino ANTLR4 SqlBase grammar (Presto branch) |
| 4 | [org.apache.calcite:calcite-core](https://calcite.apache.org/javadocAggregate/org/apache/calcite/sql/parser/SqlParser.html) | 1.42.0 | 1,250 | `SqlParser.create(local SQL text, SqlParser.config()).parseStmtList() -> SqlNodeList`; dialect: SqlParser.config() default (Calcite default lexical policy and SqlConformanceEnum.DEFAULT) | Apache Calcite JavaCC grammar (SqlParserImpl) |
| 5 | [org.apache.hive:hive-exec](https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r4.2.1/api/org/apache/hadoop/hive/ql/parse/ParseDriver.html) | 4.2.1 | 1,146 | `new ParseDriver().parse(local SQL text without its terminating semicolon).getTree() -> ASTNode`; dialect: HiveQL (ParseDriver.parse without a Configuration: default lexer, standard quoted-identifier handling) | Apache Hive ANTLR3 HiveQL grammar (HiveParser) |
| 6 | [com.github.jsqlparser:jsqlparser](https://jsqlparser.github.io/JSqlParser/usage.html) | 5.4 | 950 | `CCJSqlParserUtil.parseStatements(local SQL text) -> Statements`; dialect: JSqlParser default parser features (no dialect switch; CCJSqlParserUtil.parseStatements without a parser consumer) | JSqlParser JavaCC grammar (CCJSqlParser) |
| 7 | [org.apache.spark:spark-catalyst_2.12](https://javadoc.io/doc/org.apache.spark/spark-catalyst_2.12/3.5.9/org/apache/spark/sql/catalyst/parser/CatalystSqlParser$.html) | 3.5.9 | 529 | `CatalystSqlParser.parsePlan(local SQL text) -> LogicalPlan`; dialect: Spark SQL (CatalystSqlParser with default SQLConf; ANSI mode off) | Spark SQL ANTLR4 SqlBase grammar (AstBuilder to unresolved LogicalPlan) |
| 8 | [io.trino:trino-parser](https://javadoc.io/doc/io.trino/trino-parser/484/io/trino/sql/parser/SqlParser.html) | 484 | 525 | `new SqlParser().createStatement(local SQL text without its terminating semicolon) -> Statement`; dialect: Trino SQL (the only grammar; no parsing options) | Presto/Trino ANTLR4 SqlBase grammar (Trino branch) |
| 9 | [org.apache.flink:flink-sql-parser](https://nightlies.apache.org/flink/flink-docs-release-2.3/api/java/org/apache/flink/sql/parser/impl/FlinkSqlParserImpl.html) | 2.3.0 | 188 | `SqlParser.create(local SQL text, config with FlinkSqlParserImpl.FACTORY, FlinkSqlConformance.DEFAULT, Lex.JAVA).parseStmtList() -> SqlNodeList`; dialect: Flink SQL (FlinkSqlParserImpl.FACTORY, FlinkSqlConformance.DEFAULT, Lex.JAVA as in Flink's planner) | Apache Calcite JavaCC grammar (Flink-generated FlinkSqlParserImpl) |
| 10 | [org.apache.shardingsphere:shardingsphere-sql-parser-engine](https://shardingsphere.apache.org/document/5.3.2/en/reference/sharding/parse/) | 5.3.2 | 135 | `SQLParserEngine("MySQL", CacheOption).parse(local SQL text, false) -> ParseASTNode; SQLVisitorEngine("MySQL", "STATEMENT", false, Properties).visit(tree) -> SQLStatement`; dialect: MySQL (SQLParserEngine and SQLVisitorEngine with databaseType "MySQL", visitor type STATEMENT) | Apache ShardingSphere ANTLR4 dialect grammars (MySQL module) |

Receipts: [org.jooq:jooq](../../../projects/sql/java/jooq/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/jooq/differential.json), [com.alibaba:druid](../../../projects/sql/java/druid/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/druid/differential.json), [com.facebook.presto:presto-parser](../../../projects/sql/java/presto_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/presto_parser/differential.json), [org.apache.calcite:calcite-core](../../../projects/sql/java/calcite/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/calcite/differential.json), [org.apache.hive:hive-exec](../../../projects/sql/java/hive_exec/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/hive_exec/differential.json), [com.github.jsqlparser:jsqlparser](../../../projects/sql/java/jsqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/jsqlparser/differential.json), [org.apache.spark:spark-catalyst_2.12](../../../projects/sql/java/spark_catalyst/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/spark_catalyst/differential.json), [io.trino:trino-parser](../../../projects/sql/java/trino_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/trino_parser/differential.json), [org.apache.flink:flink-sql-parser](../../../projects/sql/java/flink_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/flink_sql_parser/differential.json) and [org.apache.shardingsphere:shardingsphere-sql-parser-engine](../../../projects/sql/java/shardingsphere_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/java/shardingsphere_sql_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| org.jooq:jooq | 4,574 | selected | jOOQ hand-written parser |
| org.apache.spark:spark-sql_2.12 | 3,567 | unresolved | Spark SQL ANTLR grammar |
| com.alibaba:druid | 1,945 | selected | Druid hand-written SQL parser |
| com.facebook.presto:presto-parser | 1,453 | selected | Presto/Trino ANTLR grammar |
| org.apache.calcite:calcite-core | 1,250 | selected | Calcite JavaCC grammar |
| org.apache.hive:hive-exec | 1,146 | selected | Apache Hive ANTLR3 HiveQL grammar |
| com.github.jsqlparser:jsqlparser | 950 | selected | JSqlParser JavaCC grammar |
| org.apache.spark:spark-catalyst_2.12 | 529 | selected | Spark SQL ANTLR grammar |
| io.trino:trino-parser | 525 | selected | Presto/Trino ANTLR grammar |
| io.prestosql:presto-parser | 282 | excluded | Presto/Trino ANTLR grammar |
| org.apache.spark:spark-catalyst_2.13 | 278 | excluded | Spark SQL ANTLR grammar |
| org.apache.flink:flink-sql-parser | 188 | selected | Calcite JavaCC grammar (Flink-generated FlinkSqlParserImpl) |
| org.apache.shardingsphere:shardingsphere-sql-parser-engine | 135 | selected | ShardingSphere ANTLR grammars |
| org.apache.spark:spark-sql-api_2.13 | 121 | excluded | Spark SQL ANTLR grammar |
| com.github.vertical-blank:sql-formatter | 111 | excluded | — |
| org.apache.shardingsphere:shardingsphere-parser-sql-engine | 64 | excluded | ShardingSphere ANTLR grammars |
| com.google.zetasql:zetasql-client | 51 | unresolved | ZetaSQL (C++ analyzer) |
| org.apache.shardingsphere:shardingsphere-sql-parser-mysql | 27 | excluded | ShardingSphere ANTLR grammars |
| org.apache.calcite:calcite-babel | 16 | unresolved | Apache Calcite JavaCC grammar (Babel) |
| org.apache.shardingsphere:shardingsphere-parser-sql-engine-core | 15 | excluded | ShardingSphere ANTLR grammars |
| org.apache.shardingsphere:shardingsphere-parser-sql-engine-mysql | 9 | excluded | ShardingSphere ANTLR grammars |
| net.sf.jsqlparser:jsqlparser | 8 | excluded | JSqlParser JavaCC grammar |
| org.apache.hive:hive-parser | 0 | excluded | Apache Hive ANTLR3 HiveQL grammar |
| io.github.melin.superior:superior-sql-parser | 0 | excluded | — |
| com.alibaba:fastsql | — | unresolved | Druid hand-written SQL parser (fork) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
