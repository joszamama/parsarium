FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib /work/underlying-lib \
    && curl --fail --location --retry 3 https://maven.jzy3d.org/releases/org/jzy3d/jzy3d-core/2.2.1/jzy3d-core-2.2.1.jar -o /work/lib/jzy3d-core-2.2.1.jar \
    && echo '1b0e31bce5745693d4c35872f6bf35f953c90d9eadcb6bee2383cd52f06bcf0e  /work/lib/jzy3d-core-2.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://maven.jzy3d.org/releases/org/smurn/jply/0.2.1/jply-0.2.1.jar -o /work/underlying-lib/jply-0.2.1.jar \
    && echo 'c62398ff7279dbab239127185316cbf654546dc3e025dc35257a02303dc23e51  /work/underlying-lib/jply-0.2.1.jar' | sha256sum --check \
    && cp /work/underlying-lib/jply-0.2.1.jar /work/lib/jply-0.2.1.jar \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar -o /work/lib/log4j-api-2.17.1.jar \
    && echo 'b0d8a4c8ab4fb8b1888d0095822703b0e6d4793c419550203da9e69196161de4  /work/lib/log4j-api-2.17.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar -o /work/lib/log4j-core-2.17.1.jar \
    && echo 'c967f223487980b9364e94a7c7f9a8a01fd3ee7c19bdbf0b0f9f8cb8511f3d41  /work/lib/log4j-core-2.17.1.jar' | sha256sum --check
# Jzy3d Core sources from its published sources JAR. jPLY 0.2.1 is published by the
# Jzy3d Maven repository without a sources JAR; its source is the jzy3d/jPLY commit
# that deployed it, whose jply/pom.xml is byte-identical to the published 0.2.1 POM.
RUN curl --fail --location --retry 3 https://maven.jzy3d.org/releases/org/jzy3d/jzy3d-core/2.2.1/jzy3d-core-2.2.1-sources.jar -o /work/parser-sources.jar \
    && echo 'e2b0929dc3efb13c0d5b8f318b7b0a503d26d0435d00502441bd5d0935196840  /work/parser-sources.jar' | sha256sum --check \
    && mkdir -p /work/parser-source/module && unzip -q /work/parser-sources.jar -d /work/parser-source/module \
    && echo 'c92e1e55a872cd4722b420622a4e3a393c2a63237a8d4d38e2e4ecf003b5450f  /work/parser-source/module/org/jzy3d/io/ply/Ply.java' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/jzy3d/jPLY/tar.gz/8bc38f3568c44c495fa41ba4393782a694ade0e3 -o /work/jply-source.tar.gz \
    && echo '69f61fdd1a2f0da5c20d0f5328aafedc8070a18305183fed8556c1e8a1dddc67  /work/jply-source.tar.gz' | sha256sum --check \
    && mkdir /work/jply-source && tar -xzf /work/jply-source.tar.gz -C /work/jply-source --strip-components=1 \
    && echo 'f452974dcc47151189c5fc2265c61d6c99c3458bf57d625d3a930b936ab29599  /work/jply-source/jply/pom.xml' | sha256sum --check \
    && echo '7e81246d09877fbb829bc4024423b9dabc38979a6669fa73f04a00c1e28a8e6f  /work/jply-source/jply/src/main/java/org/smurn/jply/PlyReaderFile.java' | sha256sum --check \
    && echo 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  /work/jply-source/LICENSE.txt' | sha256sum --check \
    && cp -R /work/jply-source/jply/src/main/java /work/parser-source/underlying
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Jzy3dPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/underlying-lib /work/underlying-lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
