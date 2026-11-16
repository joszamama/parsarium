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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2.jar -o /work/lib/ffmpeg-0.9.2.jar \
    && echo '23912a91fc755df4a172c283269890580b3b8cf7ee257003789949c4b029ca9f  /work/lib/ffmpeg-0.9.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/33.5.0-jre/guava-33.5.0-jre.jar -o /work/lib/guava-33.5.0-jre.jar \
    && echo '1e301f0c52ac248b0b14fdc3d12283c77252d4d6f48521d572e7d8c4c2cc4ac7  /work/lib/guava-33.5.0-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.3/failureaccess-1.0.3.jar -o /work/lib/failureaccess-1.0.3.jar \
    && echo 'cbfc3906b19b8f55dd7cfd6dfe0aa4532e834250d7f080bd8d211a3e246b59cb  /work/lib/failureaccess-1.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar -o /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar \
    && echo 'b372a037d4230aa57fbeffdef30fd6123f9c0c2db85d0aced00c91b974f33f99  /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jspecify/jspecify/1.0.0/jspecify-1.0.0.jar -o /work/lib/jspecify-1.0.0.jar \
    && echo '1fad6e6be7557781e4d33729d49ae1cdc8fdda6fe477bb0cc68ce351eafdfbab  /work/lib/jspecify-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.41.0/error_prone_annotations-2.41.0.jar -o /work/lib/error_prone_annotations-2.41.0.jar \
    && echo 'a56e782b5b50811ac204073a355a21d915a2107fce13ec711331ad036f660fcc  /work/lib/error_prone_annotations-2.41.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/j2objc/j2objc-annotations/3.1/j2objc-annotations-3.1.jar -o /work/lib/j2objc-annotations-3.1.jar \
    && echo '84d3a150518485f8140ea99b8a985656749629f6433c92b80c75b36aba3b099b  /work/lib/j2objc-annotations-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.21.0/commons-io-2.21.0.jar -o /work/lib/commons-io-2.21.0.jar \
    && echo '7d643a2afea8b058b762aa6fb90e5b256f6c729739f8b3784c3370ddc609e88d  /work/lib/commons-io-2.21.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.20.0/commons-lang3-3.20.0.jar -o /work/lib/commons-lang3-3.20.0.jar \
    && echo '69e5c9fa35da7a51a5fd2099dfe56a2d8d32cf233e2f6d770e796146440263f4  /work/lib/commons-lang3-3.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/code/gson/gson/2.13.2/gson-2.13.2.jar -o /work/lib/gson-2.13.2.jar \
    && echo 'dd0ce1b55a3ed2080cb70f9c655850cda86c206862310009dcb5e5c95265a5e0  /work/lib/gson-2.13.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/modelmapper/modelmapper/3.2.6/modelmapper-3.2.6.jar -o /work/lib/modelmapper-3.2.6.jar \
    && echo '65cf65bf2faa2414776eb63cf2c799361394b987700b48e415cdc77d6f8cf583  /work/lib/modelmapper-3.2.6.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-sources.jar -o /work/parser-sources.jar \
    && echo 'c863bf48b6fca24457c579a0167f21ba41fb7bbb646722e47a72689361caeae6  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY BrampMp3Adapter.java GenericHarness.java /work/src/
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
