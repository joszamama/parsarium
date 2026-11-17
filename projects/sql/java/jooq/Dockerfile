FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# jOOQ open-source edition 3.21.9 (Apache-2.0). Its POM's non-optional runtime
# dependencies are r2dbc-spi (with reactive-streams) and slf4j-api; the parser path
# runs without slf4j (jOOQ falls back to java.util.logging).
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jooq/jooq/3.21.9/jooq-3.21.9.jar -o /work/lib/jooq-3.21.9.jar \
    && echo 'e6cde9651d6795c8a6d3b10043c1edb1f3c2211fa28b15e6d537f078b1584583  /work/lib/jooq-3.21.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/r2dbc/r2dbc-spi/1.0.0.RELEASE/r2dbc-spi-1.0.0.RELEASE.jar -o /work/lib/r2dbc-spi-1.0.0.RELEASE.jar \
    && echo 'a5846c59fea336431a4ae72ca14edbf5299b78486fa308eafb383f4ae0ea74e5  /work/lib/r2dbc-spi-1.0.0.RELEASE.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/reactivestreams/reactive-streams/1.0.4/reactive-streams-1.0.4.jar -o /work/lib/reactive-streams-1.0.4.jar \
    && echo 'f75ca597789b3dac58f61857b9ac2e1034a68fa672db35055a8fb4509e325f28  /work/lib/reactive-streams-1.0.4.jar' | sha256sum --check
# Coverage subject: jOOQ (ParserImpl and the query object model it builds).
# Multi-release and module-info entries under META-INF are dropped so JaCoCo sees one class per name.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jooq/jooq/3.21.9/jooq-3.21.9-sources.jar -o /work/parser-sources.jar \
    && echo '8e58ed6849cdb8ad70023441569043307cace0ff3e8324d796157ae736495103  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/jooq-3.21.9.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/org/jooq/impl/ParserImpl.java
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
ENV JAVA_TOOL_OPTIONS="-Dorg.jooq.no-logo=true -Dorg.jooq.no-tips=true"
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
