FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir -p /work/lib /work/parser-source/module /work/parser-source/underlying \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/dataformat/jackson-dataformat-xml/2.23.0/jackson-dataformat-xml-2.23.0.jar -o /work/lib/jackson-dataformat-xml-2.23.0.jar \
    && echo 'bb77d8a97ca15f28f591055fb60a6585f6aab0758c24a994c4aa8efdb63d5979  /work/lib/jackson-dataformat-xml-2.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-core/2.23.0/jackson-core-2.23.0.jar -o /work/lib/jackson-core-2.23.0.jar \
    && echo '449798beb4c4ec26de9cc25b39ca2198036883fb905ca968cbef7136d19a25d9  /work/lib/jackson-core-2.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.23.0/jackson-databind-2.23.0.jar -o /work/lib/jackson-databind-2.23.0.jar \
    && echo 'abd1edd2736c764da03fe6cb7a9de70d48dd0a198aed131604c564bff62f9cc1  /work/lib/jackson-databind-2.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.23/jackson-annotations-2.23.jar -o /work/lib/jackson-annotations-2.23.jar \
    && echo 'e5b60c3088e0887b290ff9226394354589a1dad583743944b7f5538661056b4c  /work/lib/jackson-annotations-2.23.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/woodstox/woodstox-core/7.3.0/woodstox-core-7.3.0.jar -o /work/lib/woodstox-core-7.3.0.jar \
    && echo '246cb4845991ab52196ef90ee8a361164512b5cc7ec0547c9fab8f3db75f2679  /work/lib/woodstox-core-7.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/woodstox/stax2-api/4.3.1/stax2-api-4.3.1.jar -o /work/lib/stax2-api-4.3.1.jar \
    && echo '1953d9d443149769c8418fd4fb69284ba2f98adbbed304e9a050c360e28541c6  /work/lib/stax2-api-4.3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/dataformat/jackson-dataformat-xml/2.23.0/jackson-dataformat-xml-2.23.0-sources.jar -o /work/module-sources.jar \
    && echo '6054a0509958f6e3f474792996fa883962cb0dca305e8ae28b3900a40d2228bf  /work/module-sources.jar' | sha256sum --check \
    && unzip -q /work/module-sources.jar -d /work/parser-source/module -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/woodstox/woodstox-core/7.3.0/woodstox-core-7.3.0-sources.jar -o /work/underlying-sources.jar \
    && echo 'b90255fb33154a1fd7440a268e420f071bdb6aa0ddce04c3a6fc09757ef6c3e5  /work/underlying-sources.jar' | sha256sum --check \
    && unzip -q /work/underlying-sources.jar -d /work/parser-source/underlying -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY XmlAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
