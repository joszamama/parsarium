FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Apache ShardingSphere shardingsphere-sql-parser-engine 5.3.2 (Apache-2.0) with the MySQL dialect module the
# 5.3.2 parser documentation pairs with it (shardingsphere-sql-parser-mysql). Only the jars the parse and
# statement-visitor path loads are pinned: sql-parser-spi, sql-parser-statement, infra-util, antlr4-runtime 4.10.1,
# caffeine (parse-tree cache) and guava.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/ben-manes/caffeine/caffeine/2.9.3/caffeine-2.9.3.jar -o /work/lib/caffeine-2.9.3.jar \
    && echo '1e0a7bbef1dd791653143f3f05d0e489934bf5481e58a87c9e619cd46b68729b  /work/lib/caffeine-2.9.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/30.0-jre/guava-30.0-jre.jar -o /work/lib/guava-30.0-jre.jar \
    && echo '56b292df9ec29d102820c1fd7dd581cd749d5c416c7b3aeac008dbda3b984cc2  /work/lib/guava-30.0-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr4-runtime/4.10.1/antlr4-runtime-4.10.1.jar -o /work/lib/antlr4-runtime-4.10.1.jar \
    && echo 'da66be0c98acfb29bc708300d05f1a3269c40f9984a4cb9251cf2ba1898d1334  /work/lib/antlr4-runtime-4.10.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-infra-util/5.3.2/shardingsphere-infra-util-5.3.2.jar -o /work/lib/shardingsphere-infra-util-5.3.2.jar \
    && echo '7574e60405f2f11c83584c9b0377947e67af48386c514f68ec901dc20b34ff25  /work/lib/shardingsphere-infra-util-5.3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-engine/5.3.2/shardingsphere-sql-parser-engine-5.3.2.jar -o /work/lib/shardingsphere-sql-parser-engine-5.3.2.jar \
    && echo '0c317cfeb1a3af69d6b1be58cdc9178e668881439811d24b5cd4a3a45d3cbf61  /work/lib/shardingsphere-sql-parser-engine-5.3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-mysql/5.3.2/shardingsphere-sql-parser-mysql-5.3.2.jar -o /work/lib/shardingsphere-sql-parser-mysql-5.3.2.jar \
    && echo '81e7cced58693c5be7e6eb7c017e2b5ea3a932dab2d7e714e1b5238371742d0d  /work/lib/shardingsphere-sql-parser-mysql-5.3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-spi/5.3.2/shardingsphere-sql-parser-spi-5.3.2.jar -o /work/lib/shardingsphere-sql-parser-spi-5.3.2.jar \
    && echo '84c9d36308ac0c820a879fe534ed843a90aa3a61e65a5c1b3d6c46d235f8e953  /work/lib/shardingsphere-sql-parser-spi-5.3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-statement/5.3.2/shardingsphere-sql-parser-statement-5.3.2.jar -o /work/lib/shardingsphere-sql-parser-statement-5.3.2.jar \
    && echo '2b4daaa602c7688359e4383fd1d755f2b5f5fcf0b7a1f671e60ee13a091731f9  /work/lib/shardingsphere-sql-parser-statement-5.3.2.jar' | sha256sum --check
# Coverage subject: ShardingSphere's org.apache.shardingsphere.sql.parser classes from the engine, the MySQL dialect module (ANTLR-generated MySQLStatementParser and lexer, MySQL statement visitor) and the statement model.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-engine/5.3.2/shardingsphere-sql-parser-engine-5.3.2-sources.jar -o /work/parser-sources.jar \
    && echo 'de028b6adb93f311137cdb4382c23eaefc8526c0947bcc0f508c42bf535a1966  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/shardingsphere-sql-parser-engine-5.3.2.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-mysql/5.3.2/shardingsphere-sql-parser-mysql-5.3.2-sources.jar -o /work/extra-sources-0.jar \
    && echo '24029199c3506fca175275f8e258684542207ffd7d8cf90806acf217cec51f35  /work/extra-sources-0.jar' | sha256sum --check \
    && unzip -qo /work/extra-sources-0.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -qo /work/lib/shardingsphere-sql-parser-mysql-5.3.2.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/shardingsphere/shardingsphere-sql-parser-statement/5.3.2/shardingsphere-sql-parser-statement-5.3.2-sources.jar -o /work/extra-sources-1.jar \
    && echo '5d10f271abc4440d44fb079377bf9dfb0ffbc5e168f4c34a3f87ed6b32b59319  /work/extra-sources-1.jar' | sha256sum --check \
    && unzip -qo /work/extra-sources-1.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -qo /work/lib/shardingsphere-sql-parser-statement-5.3.2.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/org/apache/shardingsphere/sql/parser/autogen/MySQLStatementParser.java
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SqlHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
