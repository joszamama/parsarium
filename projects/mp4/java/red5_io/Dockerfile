FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/red5/red5-io/2.0.40/red5-io-2.0.40.jar -o /work/lib/red5-io-2.0.40.jar \
    && echo 'f3d1ad0fe4cf846b4622df2bc2ee4744382d013366aa05920995b56376dcf219  /work/lib/red5-io-2.0.40.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.jar -o /work/lib/jcodec-0.2.5.jar \
    && echo '890329dad124e8b739c1d6602a59a53c8a474daddff265c2561e21c498496c81  /work/lib/jcodec-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/mina/mina-core/2.0.28/mina-core-2.0.28.jar -o /work/lib/mina-core-2.0.28.jar \
    && echo 'a9aba4ef90ed6e96cf94934b91f9431bf60e87668dcf33e02e249a5526e0952c  /work/lib/mina-core-2.0.28.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.17.0/commons-lang3-3.17.0.jar -o /work/lib/commons-lang3-3.17.0.jar \
    && echo '6ee731df5c8e5a2976a1ca023b6bb320ea8d3539fbe64c8a1d5cb765127c33b4  /work/lib/commons-lang3-3.17.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.17/slf4j-api-2.0.17.jar -o /work/lib/slf4j-api-2.0.17.jar \
    && echo '7b751d952061954d5abfed7181c1f645d336091b679891591d63329c622eb832  /work/lib/slf4j-api-2.0.17.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/ben-manes/caffeine/caffeine/3.1.8/caffeine-3.1.8.jar -o /work/lib/caffeine-3.1.8.jar \
    && echo '7dd15f9df1be238ffaa367ce6f556737a88031de4294dad18eef57c474ddf1d3  /work/lib/caffeine-3.1.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/checkerframework/checker-qual/3.37.0/checker-qual-3.37.0.jar -o /work/lib/checker-qual-3.37.0.jar \
    && echo 'e4ce1376cc2735e1dde220b62ad0913f51297704daad155a33f386bc5db0d9f7  /work/lib/checker-qual-3.37.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.21.1/error_prone_annotations-2.21.1.jar -o /work/lib/error_prone_annotations-2.21.1.jar \
    && echo 'd1f3c66aa91ac52549e00ae3b208ba4b9af7d72d68f230643553beb38e6118ac  /work/lib/error_prone_annotations-2.21.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-beanutils/commons-beanutils/1.10.1/commons-beanutils-1.10.1.jar -o /work/lib/commons-beanutils-1.10.1.jar \
    && echo '707a09e86ed1cf5516cdabdf1710d8fe201b6e26e7233870dce1d0ccf2a468d1  /work/lib/commons-beanutils-1.10.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.3.4/commons-logging-1.3.4.jar -o /work/lib/commons-logging-1.3.4.jar \
    && echo 'bc2dfe32f1ef06509e6a065144c1adf7b420eabf11a87f30bd127f8faa332016  /work/lib/commons-logging-1.3.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar -o /work/lib/commons-collections-3.2.2.jar \
    && echo 'eeeae917917144a68a741d4c0dff66aa5c5c5fd85593ff217bced3fc8ca783b8  /work/lib/commons-collections-3.2.2.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/red5/red5-io/2.0.40/red5-io-2.0.40-sources.jar -o /work/parser-sources.jar \
    && echo 'c36980d1f3505e022e98391cc054b0b9ae6a4a99dee2812481b96635482004c2  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Red5IoMp4Adapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
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
