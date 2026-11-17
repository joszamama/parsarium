FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.23.0/jackson-databind-2.23.0.jar -o /work/lib/jackson-databind-2.23.0.jar \
    && echo 'abd1edd2736c764da03fe6cb7a9de70d48dd0a198aed131604c564bff62f9cc1  /work/lib/jackson-databind-2.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-core/2.23.0/jackson-core-2.23.0.jar -o /work/lib/jackson-core-2.23.0.jar \
    && echo '449798beb4c4ec26de9cc25b39ca2198036883fb905ca968cbef7136d19a25d9  /work/lib/jackson-core-2.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.23/jackson-annotations-2.23.jar -o /work/lib/jackson-annotations-2.23.jar \
    && echo 'e5b60c3088e0887b290ff9226394354589a1dad583743944b7f5538661056b4c  /work/lib/jackson-annotations-2.23.jar' | sha256sum --check
# Coverage subject: jackson-databind (untyped value mapping) and jackson-core
# (the JSON tokenizer it drives). Multi-release overlays are dropped so JaCoCo
# sees one class per name.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.23.0/jackson-databind-2.23.0-sources.jar -o /work/parser-sources.jar \
    && echo '1f2f827e0e75c4dc2ee7d43a3cdafeb92d994a58dcab3a1a1b64ce0976c977ab  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-core/2.23.0/jackson-core-2.23.0-sources.jar -o /work/core-sources.jar \
    && echo 'eaf7d94abf63f638d76ce74bbf301b779b29c45e59a84b8a1413bf49f2081260  /work/core-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q -o /work/core-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/jackson-databind-2.23.0.jar -d /work/parser-classes -x 'META-INF/*' \
    && unzip -q -o /work/lib/jackson-core-2.23.0.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY JsonAdapter.java GenericHarness.java /work/src/
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
