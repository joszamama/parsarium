FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Presto presto-parser 0.300 (Apache-2.0) with its Maven runtime closure resolved by mvn
# dependency:copy-dependencies (presto-spi, presto-common, antlr4-runtime 4.13.2, guava, slice, airlift).
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/airlift/drift/drift-api/0.231/drift-api-0.231.jar -o /work/lib/drift-api-0.231.jar \
    && echo 'f98c2623a45038a7bd73d36df8ce62448d8a1c1be3fc297a3e52f5bb676e4c0c  /work/lib/drift-api-0.231.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/airlift/log/0.231/log-0.231.jar -o /work/lib/log-0.231.jar \
    && echo '8cc7d64c46a8736210c617b225090c0dc8c2a00b9fb17a64ebabc53b72f690f8  /work/lib/log-0.231.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/airlift/units/0.231/units-0.231.jar -o /work/lib/units-0.231.jar \
    && echo 'fc2e52159159767368d680133de614e32cf9d984f7c743243baf729bba3e2d9b  /work/lib/units-0.231.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/presto/presto-common/0.300/presto-common-0.300.jar -o /work/lib/presto-common-0.300.jar \
    && echo 'cd1e78271b047b54f22bff37b540fa761b8b8c790f683f85e782cde1b64cf461  /work/lib/presto-common-0.300.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/presto/presto-parser/0.300/presto-parser-0.300.jar -o /work/lib/presto-parser-0.300.jar \
    && echo 'bb4864fa096c702713d1ceedf7ce6930fa86c017854ea91ca0ca2c4350742329  /work/lib/presto-parser-0.300.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/presto/presto-spi/0.300/presto-spi-0.300.jar -o /work/lib/presto-spi-0.300.jar \
    && echo '50d2f60d168cf302d8c45f1f2d1597137e7261bf337daae5f1f3978b8a6e1808  /work/lib/presto-spi-0.300.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.18.9/jackson-annotations-2.18.9.jar -o /work/lib/jackson-annotations-2.18.9.jar \
    && echo '798c85b86e7420d0b4eb91e7b3e37d4bee673c61de37a616ba51a7539631e6b7  /work/lib/jackson-annotations-2.18.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar -o /work/lib/jsr305-3.0.2.jar \
    && echo '766ad2a0783f2687962c8ad74ceecc38a28b9f72a2d085ee438b7813e928d0c7  /work/lib/jsr305-3.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.18.0/error_prone_annotations-2.18.0.jar -o /work/lib/error_prone_annotations-2.18.0.jar \
    && echo '9e6814cb71816988a4fd1b07a993a8f21bb7058d522c162b1de849e19bea54ae  /work/lib/error_prone_annotations-2.18.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar -o /work/lib/failureaccess-1.0.1.jar \
    && echo 'a171ee4c734dd2da837e4b16be9df4661afab72a41adaf31eb84dfdaf936ca26  /work/lib/failureaccess-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/32.1.0-jre/guava-32.1.0-jre.jar -o /work/lib/guava-32.1.0-jre.jar \
    && echo 'f2b2fd9e4e88111cc63c4349cc3455e92aad7513708e434dfcc8014a99992301  /work/lib/guava-32.1.0-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar -o /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar \
    && echo 'b372a037d4230aa57fbeffdef30fd6123f9c0c2db85d0aced00c91b974f33f99  /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/j2objc/j2objc-annotations/2.8/j2objc-annotations-2.8.jar -o /work/lib/j2objc-annotations-2.8.jar \
    && echo 'f02a95fa1a5e95edb3ed859fd0fb7df709d121a35290eff8b74dce2ab7f4d6ed  /work/lib/j2objc-annotations-2.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/airlift/slice/0.38/slice-0.38.jar -o /work/lib/slice-0.38.jar \
    && echo 'fff7dcc43e2f2497518454cdad4f85acbe26a69fb6f5a17112d44219d1ac961b  /work/lib/slice-0.38.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jakarta/inject/jakarta.inject-api/2.0.1/jakarta.inject-api-2.0.1.jar -o /work/lib/jakarta.inject-api-2.0.1.jar \
    && echo 'f7dc98062fccf14126abb751b64fab12c312566e8cbdc8483598bffcea93af7c  /work/lib/jakarta.inject-api-2.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr4-runtime/4.13.2/antlr4-runtime-4.13.2.jar -o /work/lib/antlr4-runtime-4.13.2.jar \
    && echo 'dd3e8a13a2d669bf84fb8d834de35ce4875f27157698d206241ec8488aadcaf7  /work/lib/antlr4-runtime-4.13.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/checkerframework/checker-qual/3.33.0/checker-qual-3.33.0.jar -o /work/lib/checker-qual-3.33.0.jar \
    && echo 'e316255bbfcd9fe50d165314b85abb2b33cb2a66a93c491db648e498a82c2de1  /work/lib/checker-qual-3.33.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjdk/jol/jol-core/0.2/jol-core-0.2.jar -o /work/lib/jol-core-0.2.jar \
    && echo 'ef84e1a414319772f49bcdf651c1b0cf984a51ea562c9450d8c7fb9f3261acf2  /work/lib/jol-core-0.2.jar' | sha256sum --check
# Coverage subject: Presto's com.facebook.presto.sql parser and tree packages (ANTLR-generated SqlBase lexer/parser, AstBuilder, AST nodes).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/facebook/presto/presto-parser/0.300/presto-parser-0.300-sources.jar -o /work/parser-sources.jar \
    && echo '28c00bcb132ce292e0680b72bbccd101679dd31560c02967d60f6d58b7eda35d  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/presto-parser-0.300.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/com/facebook/presto/sql/parser/AstBuilder.java
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SqlHarness.java /work/src/
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
