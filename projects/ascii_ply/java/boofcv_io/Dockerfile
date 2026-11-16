FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-io/1.6.0/boofcv-io-1.6.0.jar -o /work/lib/boofcv-io-1.6.0.jar \
    && echo 'af381c255796a7edbe502fe397f8c2bbbaa7179c117966293123741d4e82c192  /work/lib/boofcv-io-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-types/1.6.0/boofcv-types-1.6.0.jar -o /work/lib/boofcv-types-1.6.0.jar \
    && echo '3cc121687c4683177b45065f20a734b40087ca1e0a152056664c6e5708af6f36  /work/lib/boofcv-types-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-geo/1.6.0/boofcv-geo-1.6.0.jar -o /work/lib/boofcv-geo-1.6.0.jar \
    && echo '2f5cfe260e1b9258919409849e99f7137caa134e2ae0cf700333755daf7a3a19  /work/lib/boofcv-geo-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/georegression/georegression/0.30.2/georegression-0.30.2.jar -o /work/lib/georegression-0.30.2.jar \
    && echo 'd8d871555db282bbcbc6613e19e6113074280d7f8124b67445cca30da6feaeb0  /work/lib/georegression-0.30.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ddogleg/ddogleg/1.0.0/ddogleg-1.0.0.jar -o /work/lib/ddogleg-1.0.0.jar \
    && echo 'd7b89fefe0246a26e4876ebe2ad3362aa720fc2ccf150e135eba05520eb58fb9  /work/lib/ddogleg-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-core/0.46.1/ejml-core-0.46.1.jar -o /work/lib/ejml-core-0.46.1.jar \
    && echo '60e239ad8ad7b255542cab56986edec88f14feecdf86468b1ad37a7a7afe52e2  /work/lib/ejml-core-0.46.1.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-io/1.6.0/boofcv-io-1.6.0-sources.jar -o /work/parser-sources.jar \
    && echo 'dcc4376ad41b0e8a44f9a9931ed30b87cbd193976f6536efd5df0d2d56159777  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY BoofcvPlyAdapter.java GenericHarness.java /work/src/
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
