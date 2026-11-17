FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# netty-codec-dns 4.2.21.Final and its compile dependencies from its POM
# (netty-common, netty-buffer, netty-transport, netty-codec-base; netty-resolver via transport).
RUN mkdir /work/lib && cd /work/lib \
    && for a in netty-codec-dns netty-codec-base netty-common netty-buffer netty-transport netty-resolver; do \
         curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/io/netty/$a/4.2.21.Final/$a-4.2.21.Final.jar; done \
    && printf '%s\n' \
       '46bb33437b2888c170e3531ff7b7e8c6fcf89e915803e06198faa3d228bf1a53  netty-codec-dns-4.2.21.Final.jar' \
       '319f70f98ab52c27c3a46c1fd8f0f32746b7bab39bf7e3f126f2c3f2d0ab9b23  netty-codec-base-4.2.21.Final.jar' \
       '7c501587b9496b79cc65822a4cf53b07b5067ebac9533b8484524b94ab182c74  netty-common-4.2.21.Final.jar' \
       '4b3420b8a0e3928838895749af250fac3454b61ec48a95434345f815e7205b09  netty-buffer-4.2.21.Final.jar' \
       '3bfe0b8feba613aba673b97a865073d57b07fd15aef1380800180ea02cf41ce4  netty-transport-4.2.21.Final.jar' \
       '3ba53c71a41248f10cd49e27d3d969903f327353c8bf218e378ca902b89c6abd  netty-resolver-4.2.21.Final.jar' \
       | sha256sum --check
# Coverage subject: io.netty.handler.codec.dns (header, question and record decoders).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-codec-dns/4.2.21.Final/netty-codec-dns-4.2.21.Final-sources.jar -o /work/parser-sources.jar \
    && echo '7978de41898b8fbcdd06a80448509fc92d86ee7e393a4a7252d980c5c2712b8e  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/netty-codec-dns-4.2.21.Final.jar -d /work/parser-classes -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-parent/4.2.21.Final/netty-parent-4.2.21.Final.pom -o /work/netty-parent.pom \
    && echo '855f95536c719f4f4c8f71a19de68c5afe6aa58570ffbd2365ecb13bc654bbbc  /work/netty-parent.pom' | sha256sum --check \
    && grep -q '<name>Apache License, Version 2.0</name>' /work/netty-parent.pom
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY NettyDnsHarness.java /work/src/
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
