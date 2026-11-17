FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml/1.8.3/jtoml-1.8.3.jar -o /work/lib/jtoml-1.8.3.jar \
    && echo '77c6e8b379ca4c31b45d54f4487fed785d519469bc61f2a7c23635c5cb71f24e  /work/lib/jtoml-1.8.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml-api/1.8.3/jtoml-api-1.8.3.jar -o /work/lib/jtoml-api-1.8.3.jar \
    && echo '02ba6a989b1a5f08078a169c99474a3e87cd2677c91477ff2d008aa30876ba31  /work/lib/jtoml-api-1.8.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml-internals/1.8.3/jtoml-internals-1.8.3.jar -o /work/lib/jtoml-internals-1.8.3.jar \
    && echo '8b13caf9a29fc815f61b86db0e02dfb8f6c86b7cc0ce3c7804ce4e381e0ee2ae  /work/lib/jtoml-internals-1.8.3.jar' | sha256sum --check
# Coverage subject: the three jtoml release jars (api, internals, entry point) and their release sources jars only.
RUN mkdir /work/parser-source /work/parser-classes \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml/1.8.3/jtoml-1.8.3-sources.jar -o /work/jtoml-sources.jar \
    && echo '02b5912a5e2155214e9dbc978cc15f78213a8a893e4953dc3068b6a3a9933075  /work/jtoml-sources.jar' | sha256sum --check \
    && unzip -q -o /work/jtoml-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q -o /work/lib/jtoml-1.8.3.jar -d /work/parser-classes -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml-api/1.8.3/jtoml-api-1.8.3-sources.jar -o /work/jtoml-api-sources.jar \
    && echo '350b5345e8c821eb0eccf6e9c6b876f9d9ac92c623321794ea82c1303d224549  /work/jtoml-api-sources.jar' | sha256sum --check \
    && unzip -q -o /work/jtoml-api-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q -o /work/lib/jtoml-api-1.8.3.jar -d /work/parser-classes -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml-internals/1.8.3/jtoml-internals-1.8.3-sources.jar -o /work/jtoml-internals-sources.jar \
    && echo '81c087ac68573610727aff4f2357a9a3c5ebefbee6e68e158c2978b78a7e93e1  /work/jtoml-internals-sources.jar' | sha256sum --check \
    && unzip -q -o /work/jtoml-internals-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q -o /work/lib/jtoml-internals-1.8.3.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY TomlAdapter.java GenericHarness.java /work/src/
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
