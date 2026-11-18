FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# nl.sidnlabs:dnslib 0.2.20 (GPL-3.0, Java 25 bytecode) and the compile-scope dependencies its POM names:
# commons-lang3 3.20.0, commons-codec 1.21.0, guava 33.5.0-jre (with its runtime failureaccess 1.0.3) and
# log4j-core 2.26.1 (with log4j-api 2.26.1). Lombok is provided scope (compile time only).
RUN mkdir /work/lib && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/nl/sidnlabs/dnslib/0.2.20/dnslib-0.2.20.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.20.0/commons-lang3-3.20.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.21.0/commons-codec-1.21.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/google/guava/guava/33.5.0-jre/guava-33.5.0-jre.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.3/failureaccess-1.0.3.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.26.1/log4j-core-2.26.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.26.1/log4j-api-2.26.1.jar \
    && curl --fail --location --retry 3 -o /work/dnslib-0.2.20.pom https://repo.maven.apache.org/maven2/nl/sidnlabs/dnslib/0.2.20/dnslib-0.2.20.pom \
    && printf '%s\n' \
       '84a3ce4a7cdc1a29a66dd8001315023f2f60d2b889d89687fe1af07abe933d6b  dnslib-0.2.20.jar' \
       '69e5c9fa35da7a51a5fd2099dfe56a2d8d32cf233e2f6d770e796146440263f4  commons-lang3-3.20.0.jar' \
       '4da851cb6abfb98bfe9eb77c5e5fc47f5414fa28b94e21b7fd9a646705dc167f  commons-codec-1.21.0.jar' \
       '1e301f0c52ac248b0b14fdc3d12283c77252d4d6f48521d572e7d8c4c2cc4ac7  guava-33.5.0-jre.jar' \
       'cbfc3906b19b8f55dd7cfd6dfe0aa4532e834250d7f080bd8d211a3e246b59cb  failureaccess-1.0.3.jar' \
       '2ec8c3bf5a6d7c89be8620116a2fc973f7dda1ad0261ad393c4d4726edfd3dcb  log4j-core-2.26.1.jar' \
       'f1810a4704ccce019d02bba029dc02a4f2ac0c997f647b465e7d409c1927f822  log4j-api-2.26.1.jar' \
       'b035fa491778a5c688c94a15818cdc398841cb06d4cd879d8ea6b0988be076c5  /work/dnslib-0.2.20.pom' \
       | sha256sum --check \
    && grep -q '<name>GNU General Public License, version 3 </name>' /work/dnslib-0.2.20.pom
# Coverage subject: nl.sidnlabs.dnslib (Message, Header, Question, RRset, record decoders, DNSStringUtil, NetworkData).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/nl/sidnlabs/dnslib/0.2.20/dnslib-0.2.20-sources.jar -o /work/parser-sources.jar \
    && echo '87478ae9851b7debef9a5a68b4ebac42382d6159eb87574263489d9ea8abb5ea  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/dnslib-0.2.20.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SidnDnslibHarness.java /work/src/
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
