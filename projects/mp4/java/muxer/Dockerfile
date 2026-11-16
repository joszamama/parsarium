FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/mp4parser/isoparser/1.9.56/isoparser-1.9.56.jar -o /work/lib/isoparser-1.9.56.jar \
    && echo '703368e17cbbe65bbd8b2aa251f2e7d1087a4a8b46cd99149ccca14d31efe2cc  /work/lib/isoparser-1.9.56.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/aspectj/aspectjrt/1.9.7/aspectjrt-1.9.7.jar -o /work/lib/aspectjrt-1.9.7.jar \
    && echo '66af2d9a028d1c3f9d9f05bcf75e36ba1ded6d3d4d5ee90e7fce86891390e4ba  /work/lib/aspectjrt-1.9.7.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.8.0-beta4/slf4j-api-1.8.0-beta4.jar -o /work/lib/slf4j-api-1.8.0-beta4.jar \
    && echo '602b712329c84b4a83c40464f4fdfd0fe4238c53ef397139a867064739dbf4e0  /work/lib/slf4j-api-1.8.0-beta4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/mp4parser/muxer/1.9.56/muxer-1.9.56.jar -o /work/lib/muxer-1.9.56.jar \
    && echo '2bfbef3beef976a0354b6dcb6ccc244dbe76c074d9ca750cd0cbccef4e4cc41e  /work/lib/muxer-1.9.56.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/junit/junit/4.12/junit-4.12.jar -o /work/lib/junit-4.12.jar \
    && echo '59721f0805e223d84b90677887d9ff567dc534d7c502ca903c0c2b17f05c116a  /work/lib/junit-4.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar -o /work/lib/hamcrest-core-1.3.jar \
    && echo '66fdef91e9739348df7a096aa384a5685f4e875584cce89386a7a47251c4d8e9  /work/lib/hamcrest-core-1.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0.jar -o /work/lib/metadata-extractor-2.22.0.jar \
    && echo 'af451be6b366b581d8deacccd1866a5264e6c7781fd2f46941811a1a2f7777f9  /work/lib/metadata-extractor-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/adobe/xmp/xmpcore/6.1.11/xmpcore-6.1.11.jar -o /work/lib/xmpcore-6.1.11.jar \
    && echo '8f7033c579b99fa0d9d6ddcb9448875b5e4b577c350002278ce46997d678b737  /work/lib/xmpcore-6.1.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.jar -o /work/lib/jcodec-0.2.5.jar \
    && echo '890329dad124e8b739c1d6602a59a53c8a474daddff265c2561e21c498496c81  /work/lib/jcodec-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0.jar -o /work/lib/tika-parser-audiovideo-module-4.2.0.jar \
    && echo '9c8d909e889a67a1a5c1a2db9353f08b8511038fa632f273c514f89c01900a4c  /work/lib/tika-parser-audiovideo-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/gagravarr/vorbis-java-core/0.8/vorbis-java-core-0.8.jar -o /work/lib/vorbis-java-core-0.8.jar \
    && echo '879bb0c8923fea686609e207fd9050ab246e001868341c725929405e755cf68e  /work/lib/vorbis-java-core-0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-core/4.2.0/tika-core-4.2.0.jar -o /work/lib/tika-core-4.2.0.jar \
    && echo '44f95d98ec7f6b48f3fa3fc816897ee822918dae32a9a944f9179c28dd678c86  /work/lib/tika-core-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.22.0/commons-io-2.22.0.jar -o /work/lib/commons-io-2.22.0.jar \
    && echo '2b9a7b1f726fb86216dbd2c8321eabe0221dbd5b1be81c18e1cb53811b104758  /work/lib/commons-io-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-secure-xml/1.1.0/commons-secure-xml-1.1.0.jar -o /work/lib/commons-secure-xml-1.1.0.jar \
    && echo '5fc54f0d153bb9c42379a434a05177e79bbfddec7791c383370da1f592789513  /work/lib/commons-secure-xml-1.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark/0.31.0/commonmark-0.31.0.jar -o /work/lib/commonmark-0.31.0.jar \
    && echo '11d5996813f4d6525a134b906844d87112c6acb6fdd306ad5755ef5df9b26281  /work/lib/commonmark-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-tables/0.31.0/commonmark-ext-gfm-tables-0.31.0.jar -o /work/lib/commonmark-ext-gfm-tables-0.31.0.jar \
    && echo 'd2b3e19fc2a55ca1274ef067c583b85abf8635f6dccd1f935cd36ffe8a186706  /work/lib/commonmark-ext-gfm-tables-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-strikethrough/0.31.0/commonmark-ext-gfm-strikethrough-0.31.0.jar -o /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar \
    && echo '6236e6605072708d0a172a9c57802529ab71958e71c72a5e0f90a4fbf62aa9aa  /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14.jar -o /work/lib/javacv-1.5.14.jar \
    && echo 'bb421c3d3476843e78f62768a3a3b3e1bdc373efd019dc02987035d0ea036810  /work/lib/javacv-1.5.14.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14.jar -o /work/lib/ffmpeg-8.1.2-1.5.14.jar \
    && echo '1bc7d6db5ef4d8fee1b3be8cd6b2e3ef8409cb7be630f290c4d5d82d2a2fa079  /work/lib/ffmpeg-8.1.2-1.5.14.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bytedeco/javacpp/1.5.14/javacpp-1.5.14.jar -o /work/lib/javacpp-1.5.14.jar \
    && echo 'cb95a82ce1c337690436017eb8886597de71c1463dc16a3570f6a96b7c98a82b  /work/lib/javacpp-1.5.14.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14-macosx-arm64.jar -o /work/lib/ffmpeg-8.1.2-1.5.14-macosx-arm64.jar \
    && echo 'af57468c0bb7b2e9c8c93547e6d599e2b4faa4117118555be92675850972420c  /work/lib/ffmpeg-8.1.2-1.5.14-macosx-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bytedeco/javacpp/1.5.14/javacpp-1.5.14-macosx-arm64.jar -o /work/lib/javacpp-1.5.14-macosx-arm64.jar \
    && echo '75d755656d3ddafaa51c5d2d8d340c731a0bf2d742b033a37641a905aa2a7332  /work/lib/javacpp-1.5.14-macosx-arm64.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/mp4parser/muxer/1.9.56/muxer-1.9.56-sources.jar -o /work/parser-sources.jar \
    && echo 'e5f7ad0d23f1a890fc33611f86b5be71e24c564466829c21856e5fd8cedfde70  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Mp4Adapter.java GenericHarness.java /work/src/
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
