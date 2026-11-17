FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Moshi's own JsonReader is the coverage subject. Okio and Kotlin provide
# local stream infrastructure and Kotlin runtime classes, not JSON parsing.
RUN mkdir /work/lib /work/parser-source /work/parser-classes \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/squareup/moshi/moshi/1.15.2/moshi-1.15.2.jar -o /work/lib/moshi-1.15.2.jar \
    && echo '767f7592c6c61eb693549a26d333c121f5383826bd287b899867aa326dae55e4  /work/lib/moshi-1.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/squareup/moshi/moshi/1.15.2/moshi-1.15.2-sources.jar -o /work/parser-sources.jar \
    && echo 'd658332c2b2b57f94d6c26bb747e5dbb65a2d5b47cc3e0a15036977fe832996e  /work/parser-sources.jar' | sha256sum --check \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && mv /work/parser-source/main/com /work/parser-source/com \
    && unzip -q /work/lib/moshi-1.15.2.jar -d /work/parser-classes -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/squareup/okio/okio-jvm/3.7.0/okio-jvm-3.7.0.jar -o /work/lib/okio-jvm-3.7.0.jar \
    && echo 'd8b35adc28768f43ae5afe6a7d1aa2a878ba51e0b96a4f308811f3b1f5b13e55  /work/lib/okio-jvm-3.7.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.9.21/kotlin-stdlib-1.9.21.jar -o /work/lib/kotlin-stdlib-1.9.21.jar \
    && echo '3b479313ab6caea4e5e25d3dee8ca80c302c89ba73e1af4dafaa100f6ef9296a  /work/lib/kotlin-stdlib-1.9.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk8/1.8.21/kotlin-stdlib-jdk8-1.8.21.jar -o /work/lib/kotlin-stdlib-jdk8-1.8.21.jar \
    && echo '3db752a30074f06ee6c57984aa6f27da44f4d2bbc7f5442651f6988f1cb2b7d7  /work/lib/kotlin-stdlib-jdk8-1.8.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk7/1.8.21/kotlin-stdlib-jdk7-1.8.21.jar -o /work/lib/kotlin-stdlib-jdk7-1.8.21.jar \
    && echo '33d148db0e11debd0d90677d28242bced907f9c77730000fd597867089039d86  /work/lib/kotlin-stdlib-jdk7-1.8.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar -o /work/lib/annotations-13.0.jar \
    && echo 'ace2a10dc8e2d5fd34925ecac03e4988b2c0f851650c94b8cef49ba1bd111478  /work/lib/annotations-13.0.jar' | sha256sum --check
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
