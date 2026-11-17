FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Apache Calcite calcite-core 1.42.0 (Apache-2.0). Only the jars the SQL parser path loads are pinned:
# calcite-linq4j, avatica-core, guava (with failureaccess), checker-qual, apiguardian-api and slf4j-api
# (no binding; SLF4J falls back to its no-operation logger on stderr). Planner, JDBC, JTS, Janino and
# Jackson runtime dependencies of calcite-core are not on the parser path and are omitted.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.3/failureaccess-1.0.3.jar -o /work/lib/failureaccess-1.0.3.jar \
    && echo 'cbfc3906b19b8f55dd7cfd6dfe0aa4532e834250d7f080bd8d211a3e246b59cb  /work/lib/failureaccess-1.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/33.4.8-jre/guava-33.4.8-jre.jar -o /work/lib/guava-33.4.8-jre.jar \
    && echo 'f3d7f57f67fd622f4d468dfdd692b3a5e3909246c28017ac3263405f0fe617ed  /work/lib/guava-33.4.8-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/avatica/avatica-core/1.28.0/avatica-core-1.28.0.jar -o /work/lib/avatica-core-1.28.0.jar \
    && echo '59d279a2175b148ac9f73218aba1dd302fc2536bee40cf6f01fe441f886f66a2  /work/lib/avatica-core-1.28.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/calcite-core/1.42.0/calcite-core-1.42.0.jar -o /work/lib/calcite-core-1.42.0.jar \
    && echo '2ed5489201baab842001c95f939a0829849cf3cdaed9cdbf4b9078633c35792b  /work/lib/calcite-core-1.42.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/calcite-linq4j/1.42.0/calcite-linq4j-1.42.0.jar -o /work/lib/calcite-linq4j-1.42.0.jar \
    && echo '6f54fa9f24a07ad961e0e1af499a58cfc2374a93ee280283beafe9035de3fa45  /work/lib/calcite-linq4j-1.42.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apiguardian/apiguardian-api/1.1.2/apiguardian-api-1.1.2.jar -o /work/lib/apiguardian-api-1.1.2.jar \
    && echo 'b509448ac506d607319f182537f0b35d71007582ec741832a1f111e5b5b70b38  /work/lib/apiguardian-api-1.1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/checkerframework/checker-qual/3.10.0/checker-qual-3.10.0.jar -o /work/lib/checker-qual-3.10.0.jar \
    && echo 'a4dc882ca6aac496d33381e5e5eb0604c45483b004bc3eac9368f1bb17cb2512  /work/lib/checker-qual-3.10.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.25/slf4j-api-1.7.25.jar -o /work/lib/slf4j-api-1.7.25.jar \
    && echo '18c4a0095d5c1da6b817592e767bb23d29dd2f560ad74df75ff3961dbde25b79  /work/lib/slf4j-api-1.7.25.jar' | sha256sum --check
# Coverage subject: Calcite's org.apache.calcite.sql packages (JavaCC-generated SqlParserImpl, SqlParser, SqlNode tree).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/calcite/calcite-core/1.42.0/calcite-core-1.42.0-sources.jar -o /work/parser-sources.jar \
    && echo '0af0fc287b26288c8354c3aa184c4216ef5ac01b9fb96883eb9afb51d3dae5bb  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/calcite-core-1.42.0.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/org/apache/calcite/sql/parser/impl/SqlParserImpl.java
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
