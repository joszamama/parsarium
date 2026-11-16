FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1.jar -o /work/lib/jaudiotagger-3.0.1.jar \
    && echo '68aa0fe601b05df683a843acf6f8d4793ab476f47da1ac3dab57e0b1886b0aee  /work/lib/jaudiotagger-3.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/mpatric/mp3agic/0.9.1/mp3agic-0.9.1.jar -o /work/lib/mp3agic-0.9.1.jar \
    && echo '4f0fd15747cd499983e8ff5bde0a23549aea0dccef70f99e916d9a9165da26d8  /work/lib/mp3agic-0.9.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0.jar -o /work/lib/tika-parser-audiovideo-module-4.2.0.jar \
    && echo '9c8d909e889a67a1a5c1a2db9353f08b8511038fa632f273c514f89c01900a4c  /work/lib/tika-parser-audiovideo-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0.jar -o /work/lib/metadata-extractor-2.22.0.jar \
    && echo 'af451be6b366b581d8deacccd1866a5264e6c7781fd2f46941811a1a2f7777f9  /work/lib/metadata-extractor-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/adobe/xmp/xmpcore/6.1.11/xmpcore-6.1.11.jar -o /work/lib/xmpcore-6.1.11.jar \
    && echo '8f7033c579b99fa0d9d6ddcb9448875b5e4b577c350002278ce46997d678b737  /work/lib/xmpcore-6.1.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/gagravarr/vorbis-java-core/0.8/vorbis-java-core-0.8.jar -o /work/lib/vorbis-java-core-0.8.jar \
    && echo '879bb0c8923fea686609e207fd9050ab246e001868341c725929405e755cf68e  /work/lib/vorbis-java-core-0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-core/4.2.0/tika-core-4.2.0.jar -o /work/lib/tika-core-4.2.0.jar \
    && echo '44f95d98ec7f6b48f3fa3fc816897ee822918dae32a9a944f9179c28dd678c86  /work/lib/tika-core-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.20/slf4j-api-2.0.20.jar -o /work/lib/slf4j-api-2.0.20.jar \
    && echo '7e1446499b359675d8aabe6af2de86b85e72ae8a2a932c0b40d0e5ba57097439  /work/lib/slf4j-api-2.0.20.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-nop/2.0.20/slf4j-nop-2.0.20.jar -o /work/lib/slf4j-nop-2.0.20.jar \
    && echo '6522080396fb339e99bae40d329a06d18d3190dc864020ac4ca943519d0fd85b  /work/lib/slf4j-nop-2.0.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1.jar -o /work/lib/jlayer-1.0.1.jar \
    && echo '850508c837454a1b06017c32a36876fae516de1e89a829f725fee1e6dcc52000  /work/lib/jlayer-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0.jar -o /work/lib/jave-core-4.2.0.jar \
    && echo '538dc69c6e154921a2f2d7a9cfa50dd9b39ed9a18a3d0455484fdd00f1557ffb  /work/lib/jave-core-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ws/schild/jave-nativebin-osxm1/4.2.0/jave-nativebin-osxm1-4.2.0.jar -o /work/lib/jave-nativebin-osxm1-4.2.0.jar \
    && echo '5f4c7932489f130311dc8b5864958becdaf2e683307c83fb35cab83b76779388  /work/lib/jave-nativebin-osxm1-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29.jar -o /work/lib/jaffree-2024.08.29.jar \
    && echo 'f998ba5c805f92317f748f5e768dd4011db65bd2817029eea82dc87ce3c0e734  /work/lib/jaffree-2024.08.29.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/grack/nanojson/1.9/nanojson-1.9.jar -o /work/lib/nanojson-1.9.jar \
    && echo '1828955daa537121ebcbd7da5465c4cbd768d166feec85e06cab47ca0775102f  /work/lib/nanojson-1.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.jar -o /work/lib/jcodec-0.2.5.jar \
    && echo '890329dad124e8b739c1d6602a59a53c8a474daddff265c2561e21c498496c81  /work/lib/jcodec-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2.jar -o /work/lib/codecmedia-1.2.2.jar \
    && echo 'afa71e50c5f646d0f720aef4a5d31bc59b2f6c30858ba26feb5c2f180cc5f245  /work/lib/codecmedia-1.2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sf/javamusictag/jid3lib/0.5.4/jid3lib-0.5.4.jar -o /work/lib/jid3lib-0.5.4.jar \
    && echo '40c455fc91ec3bfe1007ae02b2607fdd3bc327142779fcebf576a0d07ab4ff76  /work/lib/jid3lib-0.5.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/cz/skyba/taglib/1.0.0/taglib-1.0.0.jar -o /work/lib/taglib-1.0.0.jar \
    && echo '39112950310aca2e0dc40d5d85c3f37ee350a8a08dca3beaf22850686dfb58a2  /work/lib/taglib-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/fr/delthas/javamp3/1.0.1/javamp3-1.0.1.jar -o /work/lib/javamp3-1.0.1.jar \
    && echo 'ee259df947a4242fd03d164b2fb4c61cc42e167a0af483cc18ce0c0bfa13b1ac  /work/lib/javamp3-1.0.1.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0-sources.jar -o /work/parser-sources.jar \
    && echo '1d44016129d72f1b218df2fcf18fa9a36980d8b7824fc1122b444dd82012fe4c  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Mp3Id3v2Adapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
