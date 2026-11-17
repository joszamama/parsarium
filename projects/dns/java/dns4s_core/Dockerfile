FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dns4s-core_2.13 0.21.0 (Scala 2.13 build) and the scala-library 2.13.5 its POM names. Its Guava dependency is
# used only by the DSL package (com.github.mkroli.dns4s.dsl), which the harness does not load.
RUN mkdir /work/lib && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/github/mkroli/dns4s-core_2.13/0.21.0/dns4s-core_2.13-0.21.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.5/scala-library-2.13.5.jar \
    && curl --fail --location --retry 3 -o /work/dns4s-core_2.13-0.21.0.pom https://repo.maven.apache.org/maven2/com/github/mkroli/dns4s-core_2.13/0.21.0/dns4s-core_2.13-0.21.0.pom \
    && printf '%s\n' \
       '7375689cf977de3d4a97bb29fe5152060675e1097dacb9fec9c568a51fad8a65  dns4s-core_2.13-0.21.0.jar' \
       '52aafeef8e0d104433329b1bc31463d1b4a9e2b8f24f85432c8cfaed9fad2587  scala-library-2.13.5.jar' \
       'f53be2e20b9f3b36d789864bc685c02673fd67e8ed76d56300ea61f732d95c55  /work/dns4s-core_2.13-0.21.0.pom' \
       | sha256sum --check \
    && grep -q '<name>Apache-2.0</name>' /work/dns4s-core_2.13-0.21.0.pom \
    && grep -q '<artifactId>scala-library</artifactId>' /work/dns4s-core_2.13-0.21.0.pom \
    && grep -q '<version>2.13.5</version>' /work/dns4s-core_2.13-0.21.0.pom
# Coverage subject: com.github.mkroli.dns4s (Message, MessageBuffer, sections and resource decoders).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/mkroli/dns4s-core_2.13/0.21.0/dns4s-core_2.13-0.21.0-sources.jar -o /work/parser-sources.jar \
    && echo '204b37a5d485af632ac45c4758913aecee4b0d08f30efefee1011a682a7c22a6  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/dns4s-core_2.13-0.21.0.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Dns4sHarness.java /work/src/
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
