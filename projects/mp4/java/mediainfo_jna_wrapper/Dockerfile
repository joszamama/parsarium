FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9.jar -o /work/lib/mediainfo-jna-wrapper-2.1.9.jar \
    && echo '22903d1cc7c53e3425ec7bc127fa78e1a6e1c53b98a09a3cfd1ce062e83eda68  /work/lib/mediainfo-jna-wrapper-2.1.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.20/slf4j-api-2.0.20.jar -o /work/lib/slf4j-api-2.0.20.jar \
    && echo '7e1446499b359675d8aabe6af2de86b85e72ae8a2a932c0b40d0e5ba57097439  /work/lib/slf4j-api-2.0.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/dev/jna/jna-platform/5.19.1/jna-platform-5.19.1.jar -o /work/lib/jna-platform-5.19.1.jar \
    && echo '3b3864f5b449e9c3c24b16861524b622b086563f44e0cd8384c8efc5a6052f82  /work/lib/jna-platform-5.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/dev/jna/jna/5.19.1/jna-5.19.1.jar -o /work/lib/jna-5.19.1.jar \
    && echo '4fb141dd8ef6b0585ffceea4bc49602fbc6312fa977e2c488794ea3e6aafecae  /work/lib/jna-5.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-lib-mac-aarch64/2.1.9/mediainfo-jna-lib-mac-aarch64-2.1.9.jar -o /work/lib/mediainfo-jna-lib-mac-aarch64-2.1.9.jar \
    && echo '165d787a676bf01b3516257d16388d194882bfdc801a76818f980f0597ab94d6  /work/lib/mediainfo-jna-lib-mac-aarch64-2.1.9.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9-sources.jar -o /work/parser-sources.jar \
    && echo 'e84b9f7cc57b1f46f1716918902de94b329e7a2bfe06018951925fea2b6859a9  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY AmilesendMp4Adapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libmediainfo-dev \
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
