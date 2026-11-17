FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/sceneview/sceneview-core-android/4.69.5/sceneview-core-android-4.69.5.jar -o /work/lib/sceneview-core-android-4.69.5.jar \
    && echo '7fe48b137e92e0fdb1c49875c8109542e0532188f1674586b38418a2a1fca4b7  /work/lib/sceneview-core-android-4.69.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.4.21/kotlin-stdlib-2.4.21.jar -o /work/lib/kotlin-stdlib-2.4.21.jar \
    && echo 'bd8250210584cb659847dce9cda660f8e9906e5def7fbebcea93dc6dcb6a88a3  /work/lib/kotlin-stdlib-2.4.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/dev/romainguy/kotlin-math-jvm/1.8.0/kotlin-math-jvm-1.8.0.jar -o /work/lib/kotlin-math-jvm-1.8.0.jar \
    && echo 'b11028c56d4b506d6bf73f937fc9ce7d5eb162da3c1d7307345cddd4ddfc0fbd  /work/lib/kotlin-math-jvm-1.8.0.jar' | sha256sum --check
# The Kotlin Multiplatform sources JAR keeps commonMain/ and androidMain/ roots;
# JaCoCo maps classes by package path, so both roots are merged under one tree.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/sceneview/sceneview-core-android/4.69.5/sceneview-core-android-4.69.5-sources.jar -o /work/parser-sources.jar \
    && echo '9c7fc04014a0eed68f6dc7dce6fa3015bb5ba0dcd713dcbf238e1648150104ab  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/sources-jar /work/parser-source && unzip -q /work/parser-sources.jar -d /work/sources-jar \
    && cp -R /work/sources-jar/commonMain/. /work/parser-source/ \
    && cp -R /work/sources-jar/androidMain/. /work/parser-source/ \
    && test -f /work/parser-source/io/github/sceneview/core/ply/PlyLoader.kt
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SceneviewPlyAdapter.java GenericHarness.java /work/src/
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
