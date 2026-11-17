FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/snakeyaml/snakeyaml-engine/3.2/snakeyaml-engine-3.2.jar -o /work/lib/snakeyaml-engine-3.2.jar \
    && echo '88d816316a19c6e7c48b04dc7374522ad436fa51ab105407e95b991f86d21167  /work/lib/snakeyaml-engine-3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/snakeyaml/snakeyaml-engine/3.2/snakeyaml-engine-3.2-sources.jar -o /work/parser-sources.jar \
    && echo '6b05d61b1000299f06c1bf6762d0c87dcfa7c70d259beffe633078afb23e8a15  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/snakeyaml/snakeyaml-engine/3.2/snakeyaml-engine-3.2.pom -o /work/parser.pom \
    && echo 'a9d99fd7ba9c27aad1bf093268079c46e0199fa7814c6e9283094586b8b41568  /work/parser.pom' | sha256sum --check \
    && grep -q '<name>Apache License, Version 2.0</name>' /work/parser.pom \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/snakeyaml-engine-3.2.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY YamlAdapter.java GenericHarness.java /work/src/
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
