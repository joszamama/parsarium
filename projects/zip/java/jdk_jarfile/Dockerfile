FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN echo 'db87d005701923c8b38d829219b6245bbf022262eb4851be47639fe50aa9a916  /opt/java/openjdk/jmods/java.base.jmod' | sha256sum --check \
    && jmod extract --dir /work/jdk-module /opt/java/openjdk/jmods/java.base.jmod \
    && mkdir -p /work/parser-classes/java/util \
    && cp -a /work/jdk-module/classes/java/util/zip /work/parser-classes/java/util/zip \
    && mkdir -p /work/parser-classes/java/util \
    && cp -a /work/jdk-module/classes/java/util/jar /work/parser-classes/java/util/jar \
    && mkdir /work/parser-sources
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
RUN mkdir -p /work/instrumented/java/util/jar /work/jacoco-agent-unpacked \
    && java -jar /work/jacococli.jar instrument /work/parser-classes/java/util/jar/JarFile.class --dest /work/instrumented/java/util/jar \
    && cd /work/jacoco-agent-unpacked && jar xf /work/jacocoagent.jar
COPY GenericHarness.java /work/
RUN mkdir /work/classes && javac -d /work/classes /work/GenericHarness.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_TOOL_OPTIONS=-Djava.awt.headless=true
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/instrumented /work/instrumented
COPY --from=build /work/jacoco-agent-unpacked /work/jacoco-agent-unpacked
COPY --from=build /work/parser-sources /work/parser-sources
COPY --from=build /work/jacocoagent.jar /work/jacocoagent.jar
COPY --from=build /work/jacococli.jar /work/jacococli.jar
COPY --from=build /work/jazzer /work/jazzer
COPY --from=build /work/jazzer_standalone.jar /work/jazzer_standalone.jar
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
