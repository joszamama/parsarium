FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Trino trino-parser 484 (Apache-2.0) with its Maven runtime closure resolved by mvn dependency:copy-dependencies:
# trino-grammar (the ANTLR-generated SqlBase lexer and parser), antlr4-runtime 4.13.2, guava and annotations.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.50.0/error_prone_annotations-2.50.0.jar -o /work/lib/error_prone_annotations-2.50.0.jar \
    && echo '4667724877f1d37a689202da191e23efa7657c62eef93ccdac406eccfe5cdd0a  /work/lib/error_prone_annotations-2.50.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.3/failureaccess-1.0.3.jar -o /work/lib/failureaccess-1.0.3.jar \
    && echo 'cbfc3906b19b8f55dd7cfd6dfe0aa4532e834250d7f080bd8d211a3e246b59cb  /work/lib/failureaccess-1.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/33.7.2-jre/guava-33.7.2-jre.jar -o /work/lib/guava-33.7.2-jre.jar \
    && echo 'b530942257fb935f8b2cfaa5f8eb5bd59c555fd8e8d01b8ce98912e077ea606c  /work/lib/guava-33.7.2-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/j2objc/j2objc-annotations/3.1/j2objc-annotations-3.1.jar -o /work/lib/j2objc-annotations-3.1.jar \
    && echo '84d3a150518485f8140ea99b8a985656749629f6433c92b80c75b36aba3b099b  /work/lib/j2objc-annotations-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/trino/trino-grammar/484/trino-grammar-484.jar -o /work/lib/trino-grammar-484.jar \
    && echo 'a349244944289ade63fc5164aa4889e55cb0e0f3fc17102a6685c1b215ced0ab  /work/lib/trino-grammar-484.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/trino/trino-parser/484/trino-parser-484.jar -o /work/lib/trino-parser-484.jar \
    && echo 'aa221f5100092f54cfee2c6db59a5b67b83b003e4da88b587cafb120b4829de8  /work/lib/trino-parser-484.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jakarta/annotation/jakarta.annotation-api/3.0.0/jakarta.annotation-api-3.0.0.jar -o /work/lib/jakarta.annotation-api-3.0.0.jar \
    && echo 'b01f55552284cfb149411e64eabca75e942d26d2e1786b32914250e4330afaa2  /work/lib/jakarta.annotation-api-3.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr4-runtime/4.13.2/antlr4-runtime-4.13.2.jar -o /work/lib/antlr4-runtime-4.13.2.jar \
    && echo 'dd3e8a13a2d669bf84fb8d834de35ce4875f27157698d206241ec8488aadcaf7  /work/lib/antlr4-runtime-4.13.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jspecify/jspecify/1.0.1/jspecify-1.0.1.jar -o /work/lib/jspecify-1.0.1.jar \
    && echo '070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66  /work/lib/jspecify-1.0.1.jar' | sha256sum --check
# Coverage subject: Trino's io.trino.sql parser and tree packages plus the io.trino.grammar.sql ANTLR-generated lexer and parser from trino-grammar.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/trino/trino-parser/484/trino-parser-484-sources.jar -o /work/parser-sources.jar \
    && echo 'fb48151704697abceefd803651ae54a4da713d905420ebc4500151081e06eb36  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/trino-parser-484.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/trino/trino-grammar/484/trino-grammar-484-sources.jar -o /work/extra-sources-0.jar \
    && echo 'a379e6a1986fe9a864095dc7f1061bc915259de8e58335257a4ec58015c8dbc1  /work/extra-sources-0.jar' | sha256sum --check \
    && unzip -qo /work/extra-sources-0.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -qo /work/lib/trino-grammar-484.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/io/trino/sql/parser/AstBuilder.java
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
