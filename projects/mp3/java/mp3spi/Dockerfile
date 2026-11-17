FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib /work/parser-source /work/underlying-source \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4.jar -o /work/lib/mp3spi-1.9.5.4.jar \
    && echo 'f2bd4d0b63532b52eaf9c086528ed8379e5a8805af759c4dbdea5b7a40e4e87e  /work/lib/mp3spi-1.9.5.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar -o /work/parser-sources.jar \
    && echo '8609ca1910eb46147a99e574239f3d09161aaae1c7177d70e1024176e57b4f6a  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4.pom -o /work/mp3spi.pom \
    && echo '5bf1abbc17a660c27c091e9d0282ea25e6bf357ab432a052345024e3c9c23936  /work/mp3spi.pom' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/jlayer/1.0.1.4/jlayer-1.0.1.4.jar -o /work/lib/jlayer-1.0.1.4.jar \
    && echo '863a51470ab4d581c6269dcd5a0471a226932ec5b2ef3f79fe86ab559387ac5c  /work/lib/jlayer-1.0.1.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/jlayer/1.0.1.4/jlayer-1.0.1.4-sources.jar -o /work/underlying-sources.jar \
    && echo 'a02f1ff01ade473e5fd97810154838241f6e3930eafee414673bb474ae6969a2  /work/underlying-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/jlayer/1.0.1.4/jlayer-1.0.1.4.pom -o /work/jlayer.pom \
    && echo '96f6c6e455123ccd15b4f85d6f0c6e036e667fd90d4d1ea4fb62ac16b1805244  /work/jlayer.pom' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/tritonus-share/0.3.7.4/tritonus-share-0.3.7.4.jar -o /work/lib/tritonus-share-0.3.7.4.jar \
    && echo '6f626b41dc72074656059de1a25bc6f1c5abb202b57d37c538f5714f54efdab4  /work/lib/tritonus-share-0.3.7.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/tritonus-share/0.3.7.4/tritonus-share-0.3.7.4.pom -o /work/tritonus.pom \
    && echo '9c3ab23a7f8dd3fc378dede09f5c3e91c5d17a727689591752a99eb09892c3a8  /work/tritonus.pom' | sha256sum --check \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/underlying-sources.jar -d /work/underlying-source -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Mp3SpiAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/underlying-source /work/underlying-source
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
