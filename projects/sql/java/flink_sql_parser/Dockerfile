FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Apache Flink flink-sql-parser 2.3.0 (Apache-2.0) with the calcite-core 1.36.0 it is generated against and the
# jars its parser path loads: calcite-linq4j, avatica-core, guava (provided scope in the POM) with failureaccess,
# checker-qual, apiguardian-api and slf4j-api (no binding). flink-sql-parser ships its own copies of a few
# org.apache.calcite.sql classes (SqlJoin, SqlTypeName, ...), so it precedes calcite-core on every classpath.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-parser/2.3.0/flink-sql-parser-2.3.0.jar -o /work/lib/flink-sql-parser-2.3.0.jar \
    && echo '2210424a83fff71a3653179b8447914cec6a118919cf9b61d3ed2e994b05b5ae  /work/lib/flink-sql-parser-2.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar -o /work/lib/slf4j-api-1.7.36.jar \
    && echo 'd3ef575e3e4979678dc01bf1dcce51021493b4d11fb7f1be8ad982877c16a1c0  /work/lib/slf4j-api-1.7.36.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar -o /work/lib/failureaccess-1.0.1.jar \
    && echo 'a171ee4c734dd2da837e4b16be9df4661afab72a41adaf31eb84dfdaf936ca26  /work/lib/failureaccess-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/32.1.3-jre/guava-32.1.3-jre.jar -o /work/lib/guava-32.1.3-jre.jar \
    && echo '6d4e2b5a118aab62e6e5e29d185a0224eed82c85c40ac3d33cf04a270c3b3744  /work/lib/guava-32.1.3-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/avatica/avatica-core/1.23.0/avatica-core-1.23.0.jar -o /work/lib/avatica-core-1.23.0.jar \
    && echo '9e138b51f28da396fec4e29574f05d60c8ea56551c2a6213fdb90f269e63ed7f  /work/lib/avatica-core-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/calcite-core/1.36.0/calcite-core-1.36.0.jar -o /work/lib/calcite-core-1.36.0.jar \
    && echo '1322396c24f0c80c03fc4ac8ed4f35e61d97d6717b74a6da866502c8e59827b7  /work/lib/calcite-core-1.36.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/calcite-linq4j/1.36.0/calcite-linq4j-1.36.0.jar -o /work/lib/calcite-linq4j-1.36.0.jar \
    && echo '8e5a76cbfb997157a4abe9de52a6d92515a6e611f13c8b46312982d46ea6ff3f  /work/lib/calcite-linq4j-1.36.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apiguardian/apiguardian-api/1.1.2/apiguardian-api-1.1.2.jar -o /work/lib/apiguardian-api-1.1.2.jar \
    && echo 'b509448ac506d607319f182537f0b35d71007582ec741832a1f111e5b5b70b38  /work/lib/apiguardian-api-1.1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/checkerframework/checker-qual/3.37.0/checker-qual-3.37.0.jar -o /work/lib/checker-qual-3.37.0.jar \
    && echo 'e4ce1376cc2735e1dde220b62ad0913f51297704daad155a33f386bc5db0d9f7  /work/lib/checker-qual-3.37.0.jar' | sha256sum --check
# Coverage subject: Flink's flink-sql-parser classes (JavaCC-generated FlinkSqlParserImpl, Flink SqlNode extensions and its Calcite class overrides).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-parser/2.3.0/flink-sql-parser-2.3.0-sources.jar -o /work/parser-sources.jar \
    && echo 'ff7faebcc21e3bb5200a0559f32eb62f7491cc46c11dd34743cb15194122441b  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/flink-sql-parser-2.3.0.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/org/apache/flink/sql/parser/impl/FlinkSqlParserImpl.java
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
