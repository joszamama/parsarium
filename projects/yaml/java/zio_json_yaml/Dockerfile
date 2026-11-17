FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-json-yaml_2.13/1.1.2/zio-json-yaml_2.13-1.1.2.jar -o /work/lib/zio-json-yaml_2.13-1.1.2.jar \
    && echo '3d51df89b9e5712713c444ab6d3ae1ab74172f702cd7f2a7ab03206df0e0572c  /work/lib/zio-json-yaml_2.13-1.1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.18/scala-library-2.13.18.jar -o /work/lib/scala-library-2.13.18.jar \
    && echo '4e85d96ff7bc7dc627985523c3541b9917aaa08e956391380c42db21a2c4e5a0  /work/lib/scala-library-2.13.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-json_2.13/1.1.2/zio-json_2.13-1.1.2.jar -o /work/lib/zio-json_2.13-1.1.2.jar \
    && echo 'c3342866f73eb283cd3346dc1a0c3e5718dbc8dbce76ba133786e343e3d59e76  /work/lib/zio-json_2.13-1.1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/scala-lang/modules/scala-collection-compat_2.13/2.14.0/scala-collection-compat_2.13-2.14.0.jar -o /work/lib/scala-collection-compat_2.13-2.14.0.jar \
    && echo '95986ac32df70c9ebdd96edfb276cdc038deedbe600177a45f6584022f34a13f  /work/lib/scala-collection-compat_2.13-2.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio_2.13/2.1.27/zio_2.13-2.1.27.jar -o /work/lib/zio_2.13-2.1.27.jar \
    && echo '2b074fbb56ddbe50162c27de57251f8300596881ea6fdb84cf7fe81e03732046  /work/lib/zio_2.13-2.1.27.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-streams_2.13/2.1.27/zio-streams_2.13-2.1.27.jar -o /work/lib/zio-streams_2.13-2.1.27.jar \
    && echo '39582ee63fbd9f8642215adeb8b40bd95b37cca7d69410b85220fb4d66aa62f2  /work/lib/zio-streams_2.13-2.1.27.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-internal-macros_2.13/2.1.27/zio-internal-macros_2.13-2.1.27.jar -o /work/lib/zio-internal-macros_2.13-2.1.27.jar \
    && echo 'd97505ec5f65ade8a26da0e3144cc0fb0960c4075c9c4e81249f7181a727288f  /work/lib/zio-internal-macros_2.13-2.1.27.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-stacktracer_2.13/2.1.27/zio-stacktracer_2.13-2.1.27.jar -o /work/lib/zio-stacktracer_2.13-2.1.27.jar \
    && echo '098fb54489ad7b515c91bdb2cacd74fd2b4a858bce657d7d73fa09b732c7b082  /work/lib/zio-stacktracer_2.13-2.1.27.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/izumi-reflect_2.13/3.0.11/izumi-reflect_2.13-3.0.11.jar -o /work/lib/izumi-reflect_2.13-3.0.11.jar \
    && echo 'd6fa1618bcb49439ad22be62daab9c9ee1351aec18261b36cd4958619cfc8a03  /work/lib/izumi-reflect_2.13-3.0.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/izumi-reflect-thirdparty-boopickle-shaded_2.13/3.0.11/izumi-reflect-thirdparty-boopickle-shaded_2.13-3.0.11.jar -o /work/lib/izumi-reflect-thirdparty-boopickle-shaded_2.13-3.0.11.jar \
    && echo '160b16f9ace411472ecd3451b7602b9b47c81b49410e3bb684311ea68d22373f  /work/lib/izumi-reflect-thirdparty-boopickle-shaded_2.13-3.0.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/softwaremill/magnolia1_2/magnolia_2.13/1.1.14/magnolia_2.13-1.1.14.jar -o /work/lib/magnolia_2.13-1.1.14.jar \
    && echo '720b5a928347f98eb49c05e6413985ee663538c64a0b739c392053f76ea0f389  /work/lib/magnolia_2.13-1.1.14.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/yaml/snakeyaml/2.7/snakeyaml-2.7.jar -o /work/lib/snakeyaml-2.7.jar \
    && echo '2e194eba45a67dee19a4e272f4a04b18de8054e9f598b094382f6dae0b0e4b5e  /work/lib/snakeyaml-2.7.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-json-yaml_2.13/1.1.2/zio-json-yaml_2.13-1.1.2-sources.jar -o /work/parser-sources.jar \
    && echo 'df4504c6d335f7ee2c5f581731877107b6946479b87f12bb5b9c24f0edf588e8  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/zio/zio-json-yaml_2.13/1.1.2/zio-json-yaml_2.13-1.1.2.pom -o /work/parser.pom \
    && echo 'a3f14de07c81a3bb607772c2dd2dd32c003bed15a7dd7528473d33841e83ad4e  /work/parser.pom' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/yaml/snakeyaml/2.7/snakeyaml-2.7-sources.jar -o /work/underlying-sources.jar \
    && echo 'f7b972dfc3d51ad08af2f6a6e828b4ed449c718ab6b57673238e6d0460a1a626  /work/underlying-sources.jar' | sha256sum --check \
    && grep -q '<name>Apache-2.0</name>' /work/parser.pom \
    && mkdir -p /work/parser-source/module /work/parser-source/underlying \
    && unzip -q /work/parser-sources.jar -d /work/parser-source/module -x 'META-INF/*' \
    && unzip -q /work/underlying-sources.jar -d /work/parser-source/underlying -x 'META-INF/*' \
    && mkdir /work/underlying-classes \
    && unzip -q /work/lib/snakeyaml-2.7.jar -d /work/underlying-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY YamlAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/underlying-classes /work/underlying-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
