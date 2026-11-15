FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56.jar -o /work/parser.jar \
    && echo '703368e17cbbe65bbd8b2aa251f2e7d1087a4a8b46cd99149ccca14d31efe2cc  /work/parser.jar' | sha256sum --check \
    && curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56-sources.jar -o /work/parser-sources.jar \
    && echo '852e3b2daa7884a057bdaad8226ce187aa3c5774cf2fef61b8a973a8192b6831  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-sources && unzip -q /work/parser-sources.jar -d /work/parser-sources
RUN curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/aspectj/aspectjrt/1.9.7/aspectjrt-1.9.7.jar -o /work/aspectjrt.jar \
    && echo '66af2d9a028d1c3f9d9f05bcf75e36ba1ded6d3d4d5ee90e7fce86891390e4ba  /work/aspectjrt.jar' | sha256sum --check \
    && curl --fail --location --retry 3 \
      https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.8.0-beta4/slf4j-api-1.8.0-beta4.jar -o /work/slf4j.jar \
    && echo '602b712329c84b4a83c40464f4fdfd0fe4238c53ef397139a867064739dbf4e0  /work/slf4j.jar' | sha256sum --check
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
COPY IsoparserHarness.java /work/
RUN mkdir /work/classes && javac -cp /work/parser.jar:/work/aspectjrt.jar:/work/slf4j.jar -d /work/classes /work/IsoparserHarness.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/parser.jar /work/parser.jar
COPY --from=build /work/aspectjrt.jar /work/aspectjrt.jar
COPY --from=build /work/slf4j.jar /work/slf4j.jar
COPY --from=build /work/parser-sources /work/parser-sources
COPY --from=build /work/jacocoagent.jar /work/jacocoagent.jar
COPY --from=build /work/jacococli.jar /work/jacococli.jar
COPY --from=build /work/jazzer /work/jazzer
COPY --from=build /work/jazzer_standalone.jar /work/jazzer_standalone.jar
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
