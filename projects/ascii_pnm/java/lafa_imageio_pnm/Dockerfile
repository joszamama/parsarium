FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/imageio/imageio-pnm/1.0/imageio-pnm-1.0.jar -o /work/lib/imageio-pnm-1.0.jar \
    && echo '610f614ced2664d05ddca464a36f5bdf6f00a92d9dad052efe1bb4f474811071  /work/lib/imageio-pnm-1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/imageio/imageio-core/1.0/imageio-core-1.0.jar -o /work/lib/imageio-core-1.0.jar \
    && echo 'a5d6a7a5b8d4fccef8f51c28e67da369d5b7c87f6c72cccdb5f5f065edb9fd3b  /work/lib/imageio-core-1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/common/common-lang/1.0/common-lang-1.0.jar -o /work/lib/common-lang-1.0.jar \
    && echo '587557921da4752d9c3d6a9204d50afc00db27fb5af9836f8737c3ae7ae6c81b  /work/lib/common-lang-1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/common/common-io/1.0/common-io-1.0.jar -o /work/lib/common-io-1.0.jar \
    && echo 'e939649c15b8183ad480cd24d4a8f4af3725f03e662f8179d192ca0a7ff23e2e  /work/lib/common-io-1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/common/common-image/1.0/common-image-1.0.jar -o /work/lib/common-image-1.0.jar \
    && echo '0f43589165caf1602416a8ca1f02d41f8a90891c5e0c5390ce0d0afa69060a70  /work/lib/common-image-1.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/lafa/twelvemonkeyspurejava/imageio/imageio-pnm/1.0/imageio-pnm-1.0-sources.jar -o /work/parser-sources.jar \
    && echo '8de7f3af51749a99335af7992613ab9b53a2d527592e2232888cafd087f12aea  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY LafaPnmAdapter.java GenericHarness.java /work/src/
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
