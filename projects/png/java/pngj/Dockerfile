FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/ar/com/hjg/pngj/2.1.0/pngj-2.1.0.jar -o /work/pngj.jar \
    && echo 'e6b762f15e4891178dddd74e4d57318f518ce278000129efa41f85410b132ccc  /work/pngj.jar' | sha256sum --check \
    && curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/ar/com/hjg/pngj/2.1.0/pngj-2.1.0-sources.jar -o /work/pngj-sources.jar \
    && echo '4debe6db2149c45aff47567ba76adde2ec5593e801b2982dc1cc55594c94f588  /work/pngj-sources.jar' | sha256sum --check \
    && mkdir /work/pngj-sources && unzip -q /work/pngj-sources.jar -d /work/pngj-sources
RUN curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check
RUN curl --fail --location --retry 3 \
      https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz \
      -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY PngjHarness.java /work/
RUN mkdir /work/classes && javac -cp /work/pngj.jar -d /work/classes /work/PngjHarness.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/pngj.jar /work/pngj.jar
COPY --from=build /work/pngj-sources /work/pngj-sources
COPY --from=build /work/jacocoagent.jar /work/jacocoagent.jar
COPY --from=build /work/jacococli.jar /work/jacococli.jar
COPY --from=build /work/jazzer /work/jazzer
COPY --from=build /work/jazzer_standalone.jar /work/jazzer_standalone.jar
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
