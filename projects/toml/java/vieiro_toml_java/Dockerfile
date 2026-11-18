FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# net.vieiro:toml-java 13.5.1 and its one runtime dependency from the release POM, antlr4-runtime 4.13.1.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/vieiro/toml-java/13.5.1/toml-java-13.5.1.jar -o /work/lib/toml-java-13.5.1.jar \
    && echo 'ca4314a5361406387b238bc047e8b759cb4838e32a6605bf6eb8e4ebefe918f8  /work/lib/toml-java-13.5.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr4-runtime/4.13.1/antlr4-runtime-4.13.1.jar -o /work/lib/antlr4-runtime-4.13.1.jar \
    && echo '54665d2838cc66458343468efc539e454fc95b46a8a04b13c6ac43fc9be63505  /work/lib/antlr4-runtime-4.13.1.jar' | sha256sum --check
# Coverage subject: the net.vieiro.toml packages of the release jar and its release sources jar
# (own TOMLAntlrLexer.g4/TOMLAntlrParser.g4 grammar with the generated lexer and parser, and the
# TOMLVisitor/TOMLStringVisitor value builders). The antlr4-runtime jar is outside the subject.
RUN mkdir /work/parser-source /work/parser-classes \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/vieiro/toml-java/13.5.1/toml-java-13.5.1-sources.jar -o /work/toml-java-sources.jar \
    && echo '2ab8209096ef082b6c0f030c9c8034bd823e58d695975d5f346e3465ef15c407  /work/toml-java-sources.jar' | sha256sum --check \
    && unzip -q -o /work/toml-java-sources.jar -d /work/parser-source -x 'META-INF/*' 'module-info.java' \
    && unzip -q -o /work/lib/toml-java-13.5.1.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/net/vieiro/toml/TOMLVisitor.java
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
