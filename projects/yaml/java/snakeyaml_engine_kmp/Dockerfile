FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/it/krzeminski/snakeyaml-engine-kmp-jvm/5.0.0/snakeyaml-engine-kmp-jvm-5.0.0.jar -o /work/lib/snakeyaml-engine-kmp-jvm-5.0.0.jar \
    && echo '506718c275eef4118fc589f95004066079bf72b872850cd8bd89bb6fc08dec1e  /work/lib/snakeyaml-engine-kmp-jvm-5.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.4.10/kotlin-stdlib-2.4.10.jar -o /work/lib/kotlin-stdlib-2.4.10.jar \
    && echo '4ec0293bc3751423b203f1d8493251c57c42e73eb6377a6b8560d0974ff0a6df  /work/lib/kotlin-stdlib-2.4.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar -o /work/lib/annotations-13.0.jar \
    && echo 'ace2a10dc8e2d5fd34925ecac03e4988b2c0f851650c94b8cef49ba1bd111478  /work/lib/annotations-13.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/squareup/okio/okio-jvm/3.18.2/okio-jvm-3.18.2.jar -o /work/lib/okio-jvm-3.18.2.jar \
    && echo '681fed549d1d2c63710f42c9eab433d642c71af778babd67035c50f8c425aaff  /work/lib/okio-jvm-3.18.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/thauvin/erik/urlencoder/urlencoder-lib-jvm/1.6.0/urlencoder-lib-jvm-1.6.0.jar -o /work/lib/urlencoder-lib-jvm-1.6.0.jar \
    && echo '8d0fd2aeb48d19dc49c563ebc00f274947e45f716c107535c12ead63decd688d  /work/lib/urlencoder-lib-jvm-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/it/krzeminski/snakeyaml-engine-kmp-jvm/5.0.0/snakeyaml-engine-kmp-jvm-5.0.0-sources.jar -o /work/parser-sources.jar \
    && echo '4d5707c0d37211c2e779ae21124cbc8bdd783ebbb242d65d059619152148f7a8  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/it/krzeminski/snakeyaml-engine-kmp-jvm/5.0.0/snakeyaml-engine-kmp-jvm-5.0.0.pom -o /work/parser.pom \
    && echo '56482407c62efff10a9aecdce3bee89d4334110d877e14423f7df751c95fcd6e  /work/parser.pom' | sha256sum --check \
    && grep -q '<name>Apache-2.0</name>' /work/parser.pom \
    && mkdir /work/parser-source /work/parser-classes /work/kmp-sources \
    && unzip -q /work/parser-sources.jar -d /work/kmp-sources -x 'META-INF/*' \
    && cp -R /work/kmp-sources/commonMain/. /work/parser-source/ \
    && cp -R /work/kmp-sources/jvmMain/. /work/parser-source/ \
    && unzip -q /work/lib/snakeyaml-engine-kmp-jvm-5.0.0.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class'
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
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
