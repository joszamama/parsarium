FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Apache Hive hive-exec 4.2.1 (Apache-2.0), the uber jar that ships Hive's HiveQL parser classes.
# ParseDriver needs hadoop-common's Configuration (an optional hive-exec dependency) and, through
# HiveConf, woodstox, stax2, commons-collections and hadoop-shaded-guava; slf4j-api has no binding.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/hive/hive-exec/4.2.1/hive-exec-4.2.1.jar -o /work/lib/hive-exec-4.2.1.jar \
    && echo '38c114a22a8f93588c3f9829a5451edc45a6e439bd50d73ee0c63185fcca3838  /work/lib/hive-exec-4.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar -o /work/lib/slf4j-api-1.7.36.jar \
    && echo 'd3ef575e3e4979678dc01bf1dcce51021493b4d11fb7f1be8ad982877c16a1c0  /work/lib/slf4j-api-1.7.36.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/woodstox/woodstox-core/5.4.0/woodstox-core-5.4.0.jar -o /work/lib/woodstox-core-5.4.0.jar \
    && echo 'dbb958cb89f1d45238b061e146249494ff887f5f42b671a3956e98956e0d5c53  /work/lib/woodstox-core-5.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar -o /work/lib/commons-collections-3.2.2.jar \
    && echo 'eeeae917917144a68a741d4c0dff66aa5c5c5fd85593ff217bced3fc8ca783b8  /work/lib/commons-collections-3.2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-common/3.4.1/hadoop-common-3.4.1.jar -o /work/lib/hadoop-common-3.4.1.jar \
    && echo '85ab34eb0efc42651290991473341fc77491de2e0cfa7f2d02d20c57abed3aeb  /work/lib/hadoop-common-3.4.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/hadoop/thirdparty/hadoop-shaded-guava/1.3.0/hadoop-shaded-guava-1.3.0.jar -o /work/lib/hadoop-shaded-guava-1.3.0.jar \
    && echo 'a8b83aecef36f55f3e6377c850a763b995cb8eea629a43e78329c580ba651dda  /work/lib/hadoop-shaded-guava-1.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar -o /work/lib/stax2-api-4.2.1.jar \
    && echo '678567e48b51a42c65c699f266539ad3d676d4b1a5b0ad7d89ece8b9d5772579  /work/lib/stax2-api-4.2.1.jar' | sha256sum --check
# Coverage subject: the hive-parser module's classes inside hive-exec (ParseDriver, ASTNode, lexer helpers
# and the ANTLR-generated HiveLexer/HiveParser). The sources jar has grammars but no generated Java, so
# prepare-coverage.sh regenerates it with ANTLR 3.5.2 and checks each class's line table against hive-exec.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/hive/hive-parser/4.2.1/hive-parser-4.2.1-sources.jar -o /work/parser-sources.jar \
    && echo 'd2708ee7e5848e867da03824829281ec7aa342eda1175ecc4ba3168d03f3c1b4  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr-complete/3.5.2/antlr-complete-3.5.2.jar -o /work/antlr-complete-3.5.2.jar \
    && echo '26ca659f47d77384f518cf2b6463892fcd4f0b0d4d8c0de2addf697e63e7326b  /work/antlr-complete-3.5.2.jar' | sha256sum --check \
    && mkdir /work/parser-source \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && test -f /work/parser-source/org/apache/hadoop/hive/ql/parse/HiveParser.g
COPY prepare-coverage.sh /work/prepare-coverage.sh
RUN sh /work/prepare-coverage.sh \
    && test -f /work/parser-source/org/apache/hadoop/hive/ql/parse/HiveParser.java
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
# HiveConf's static initialisation (reached from ParseDriver) reflects into java.net.URI.
ENV JAVA_TOOL_OPTIONS="--add-opens=java.base/java.net=ALL-UNNAMED"
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
