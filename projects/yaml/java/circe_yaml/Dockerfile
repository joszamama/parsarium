FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-yaml_2.13/0.16.1/circe-yaml_2.13-0.16.1.jar -o /work/lib/circe-yaml_2.13-0.16.1.jar \
    && echo '24c76c830cfc8870d7a41a77a048818dc7bed82d552d9aec3f0c354379ee9490  /work/lib/circe-yaml_2.13-0.16.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.16/scala-library-2.13.16.jar -o /work/lib/scala-library-2.13.16.jar \
    && echo '1ebb2b6f9e4eb4022497c19b1e1e825019c08514f962aaac197145f88ed730f1  /work/lib/scala-library-2.13.16.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-yaml-common_2.13/0.16.1/circe-yaml-common_2.13-0.16.1.jar -o /work/lib/circe-yaml-common_2.13-0.16.1.jar \
    && echo '1d6f3e97baf68e531331ab77eec0988e0d1b4af16a6e0fd448a726b974e60e2e  /work/lib/circe-yaml-common_2.13-0.16.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-core_2.13/0.14.13/circe-core_2.13-0.14.13.jar -o /work/lib/circe-core_2.13-0.14.13.jar \
    && echo '96c888dca30eb7052851cb1984b5935ca239f191648e9faf3510ed107ddf5b7b  /work/lib/circe-core_2.13-0.14.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-numbers_2.13/0.14.13/circe-numbers_2.13-0.14.13.jar -o /work/lib/circe-numbers_2.13-0.14.13.jar \
    && echo 'd1918ae12d06083710d1f6477433df08cb2c14b84954ca3cfbfa8b16478cb4ba  /work/lib/circe-numbers_2.13-0.14.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/typelevel/cats-core_2.13/2.13.0/cats-core_2.13-2.13.0.jar -o /work/lib/cats-core_2.13-2.13.0.jar \
    && echo 'df55126bba064bc6e156b038ad76a6fd8309ce6356b776d847542e04d683735e  /work/lib/cats-core_2.13-2.13.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/typelevel/cats-kernel_2.13/2.13.0/cats-kernel_2.13-2.13.0.jar -o /work/lib/cats-kernel_2.13-2.13.0.jar \
    && echo 'dc19503af643a899910832898a39150fb6c35e5d891e0b2e3a25e43cbd518ec9  /work/lib/cats-kernel_2.13-2.13.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/yaml/snakeyaml/2.2/snakeyaml-2.2.jar -o /work/lib/snakeyaml-2.2.jar \
    && echo '1467931448a0817696ae2805b7b8b20bfb082652bf9c4efaed528930dc49389b  /work/lib/snakeyaml-2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-yaml_2.13/0.16.1/circe-yaml_2.13-0.16.1-sources.jar -o /work/parser-sources.jar \
    && echo '18111533cae998c318081f4562af9de2fb1329968091491b27aabe2fa6296bde  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/circe/circe-yaml_2.13/0.16.1/circe-yaml_2.13-0.16.1.pom -o /work/parser.pom \
    && echo 'edd87515c1b9281c08c8dfafcbe6d8c9185b24f4c03bab82eb34a44e1c9ecc69  /work/parser.pom' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/yaml/snakeyaml/2.2/snakeyaml-2.2-sources.jar -o /work/underlying-sources.jar \
    && echo '8f7cf911cf63db55fd980a926d155bd846317737351a2f48ef1c1088c414538a  /work/underlying-sources.jar' | sha256sum --check \
    && grep -q '<name>Apache-2.0</name>' /work/parser.pom \
    && mkdir -p /work/parser-source/module /work/parser-source/underlying \
    && unzip -q /work/parser-sources.jar -d /work/parser-source/module -x 'META-INF/*' \
    && unzip -q /work/underlying-sources.jar -d /work/parser-source/underlying -x 'META-INF/*' \
    && mkdir /work/underlying-classes \
    && unzip -q /work/lib/snakeyaml-2.2.jar -d /work/underlying-classes -x 'META-INF/*'
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
