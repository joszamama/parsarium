FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Official v4.0 release asset: the JVM Assimp port bundled with its runtime dependencies.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://github.com/kotlin-graphics/assimp/releases/download/v4.0/assimp-all.jar -o /work/lib/assimp-all.jar \
    && echo 'ad7aef390521eaf3741614749ced1ef0803ed9e803161d14838eaeb8a9372a56  /work/lib/assimp-all.jar' | sha256sum --check
# JaCoCo reports only the port's own assimp.* classes, mapped to the tagged Kotlin sources.
RUN mkdir /work/parser-classes && cd /work/parser-classes && unzip -q /work/lib/assimp-all.jar 'assimp/*' \
    && curl --fail --location --retry 3 https://github.com/kotlin-graphics/assimp/archive/refs/tags/v4.0.tar.gz -o /work/assimp-4.0.tar.gz \
    && echo '1edb9ad3b65adb721b91b02acf9014717e83c93de1dbc4b2278d4006ed043fad  /work/assimp-4.0.tar.gz' | sha256sum --check \
    && mkdir /work/assimp-source && tar -xzf /work/assimp-4.0.tar.gz -C /work/assimp-source --strip-components=1 \
       assimp-4.0/LICENSE.txt assimp-4.0/src/main/kotlin \
    && rm /work/assimp-4.0.tar.gz && cd /work/assimp-source && printf '%s\n' \
    '69f506f97f1d4ec3f2c7817b70b2090044cc9079cc5b8c232a98ead7244d0966  LICENSE.txt' \
    '942a6dfd239ae339f54e2adef71b7e0f85c94c7a62ad09213b77e2f02070b377  src/main/kotlin/assimp/Importer.kt' \
    '7c68cc4afcd51d86ed7b4e22ff2c9495d1b39039be2ca706d33e4810c97d0bf1  src/main/kotlin/assimp/format/ply/PlyLoader.kt' \
    '38c16a94b3b39908872fe65c01446db50c379ffb7efcf5c47c7c2a911bcabb2f  src/main/kotlin/assimp/format/ply/PlyParser.kt' \
    | sha256sum --check \
    && cp -R /work/assimp-source/src/main/kotlin /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY KotlinAssimpPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
