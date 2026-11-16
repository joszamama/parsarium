FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-nop/2.0.17/slf4j-nop-2.0.17.jar -o /work/lib/slf4j-nop-2.0.17.jar \
    && echo '3716f83649ec66161a2edefd4f49df34d1dd1c51cdcf941996c6987260f0a829  /work/lib/slf4j-nop-2.0.17.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.17/slf4j-api-2.0.17.jar -o /work/lib/slf4j-api-2.0.17.jar \
    && echo '7b751d952061954d5abfed7181c1f645d336091b679891591d63329c622eb832  /work/lib/slf4j-api-2.0.17.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0.jar -o /work/lib/jaffree-2.1.0.jar \
    && echo 'a1ee68960539510ae4c349eb57c94e87dd63d43f8008937588594b7d17eac85c  /work/lib/jaffree-2.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/26.0.2/annotations-26.0.2.jar -o /work/lib/annotations-26.0.2.jar \
    && echo '2037be378980d3ba9333e97955f3b2cde392aa124d04ca73ce2eee6657199297  /work/lib/annotations-26.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.1.21/kotlin-stdlib-2.1.21.jar -o /work/lib/kotlin-stdlib-2.1.21.jar \
    && echo '263bdc679e1f62012db7b091796279b6d71cf36f4797a98ff1ace05835f201c8  /work/lib/kotlin-stdlib-2.1.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/grack/nanojson/1.9/nanojson-1.9.jar -o /work/lib/nanojson-1.9.jar \
    && echo '1828955daa537121ebcbd7da5465c4cbd768d166feec85e06cab47ca0775102f  /work/lib/nanojson-1.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/zaxxer/nuprocess/3.0.0/nuprocess-3.0.0.jar -o /work/lib/nuprocess-3.0.0.jar \
    && echo '8a3b7ea6380996651ea7784ff7184a2aa119db16100b040d4b2d449b4142aa58  /work/lib/nuprocess-3.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/dev/jna/jna/5.11.0/jna-5.11.0.jar -o /work/lib/jna-5.11.0.jar \
    && echo 'e2bce99e4aefd4dab097019a799d317cb3b5d56c3ddd7984c69a772dceed0dd3  /work/lib/jna-5.11.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0-sources.jar -o /work/parser-sources.jar \
    && echo 'bd6a299f4d6f619d7e8e1971c099137666fbc960554b902a7c28b9eece9b5535  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY V47Mp3Adapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 ffmpeg \
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
