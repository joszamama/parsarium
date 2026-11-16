FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/psambit9791/wavfile/1.0.0/wavfile-1.0.0.jar -o /work/lib/wavfile-1.0.0.jar \
    && echo 'c36029a8c2310da9b70fdf8805b13ae17a33e3fa86e876a72a4c7f96082b50ea  /work/lib/wavfile-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apiguardian/apiguardian-api/1.0.0/apiguardian-api-1.0.0.jar -o /work/lib/apiguardian-api-1.0.0.jar \
    && echo '1f58b77470d8d147a0538d515347dd322f49a83b9e884b8970051160464b65b3  /work/lib/apiguardian-api-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/opentest4j/opentest4j/1.0.0/opentest4j-1.0.0.jar -o /work/lib/opentest4j-1.0.0.jar \
    && echo '6a05b14e8764a1fa51551ccef29e7271681d65fa907a8136136b94de92a0b862  /work/lib/opentest4j-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/maven/surefire/surefire-api/2.19.1/surefire-api-2.19.1.jar -o /work/lib/surefire-api-2.19.1.jar \
    && echo 'de34106fd8799d9cc690aded4eb329c5c2c9f96929b2fea032ec9a5bdf036613  /work/lib/surefire-api-2.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/maven/surefire/common-java5/2.19.1/common-java5-2.19.1.jar -o /work/lib/common-java5-2.19.1.jar \
    && echo '831f47a1fb1446f6bd8653ea4183c4b1601eab943da6c8ec160d7b83b19de1d0  /work/lib/common-java5-2.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1.jar -o /work/lib/jaudiotagger-3.0.1.jar \
    && echo '68aa0fe601b05df683a843acf6f8d4793ab476f47da1ac3dab57e0b1886b0aee  /work/lib/jaudiotagger-3.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.jar -o /work/lib/jcodec-0.2.5.jar \
    && echo '890329dad124e8b739c1d6602a59a53c8a474daddff265c2561e21c498496c81  /work/lib/jcodec-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/beadsproject/beads/3.2/beads-3.2.jar -o /work/lib/beads-3.2.jar \
    && echo 'e2770836eebfaaa3b703e33f6db7548bd25c0196fdeb40959e5d51ee91f134c5  /work/lib/beads-3.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1.jar -o /work/lib/jlayer-1.0.1.jar \
    && echo '850508c837454a1b06017c32a36876fae516de1e89a829f725fee1e6dcc52000  /work/lib/jlayer-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4.jar -o /work/lib/mp3spi-1.9.5.4.jar \
    && echo 'f2bd4d0b63532b52eaf9c086528ed8379e5a8805af759c4dbdea5b7a40e4e87e  /work/lib/mp3spi-1.9.5.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/jlayer/1.0.1.4/jlayer-1.0.1.4.jar -o /work/lib/jlayer-1.0.1.4.jar \
    && echo '863a51470ab4d581c6269dcd5a0471a226932ec5b2ef3f79fe86ab559387ac5c  /work/lib/jlayer-1.0.1.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/tritonus-share/0.3.7.4/tritonus-share-0.3.7.4.jar -o /work/lib/tritonus-share-0.3.7.4.jar \
    && echo '6f626b41dc72074656059de1a25bc6f1c5abb202b57d37c538f5714f54efdab4  /work/lib/tritonus-share-0.3.7.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jaudiolibs/audioservers-javasound/2.0.0/audioservers-javasound-2.0.0.jar -o /work/lib/audioservers-javasound-2.0.0.jar \
    && echo '7b3fd46292970afd81594bed7f32c15f188f5e47511d26215f8de3099d1a24d9  /work/lib/audioservers-javasound-2.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jaudiolibs/audioservers-api/2.0.0/audioservers-api-2.0.0.jar -o /work/lib/audioservers-api-2.0.0.jar \
    && echo '0b18e1530568e28e5ebf95b749880518582a9064dd35172a2b2121c74731d340  /work/lib/audioservers-api-2.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jaudiolibs/audioservers-jack/2.0.0/audioservers-jack-2.0.0.jar -o /work/lib/audioservers-jack-2.0.0.jar \
    && echo 'd30cf08e0be62df176699b15e66a7b5d43883d4ed92c45ebedadb0cf47a41b28  /work/lib/audioservers-jack-2.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jaudiolibs/jnajack/1.4.0/jnajack-1.4.0.jar -o /work/lib/jnajack-1.4.0.jar \
    && echo '3e3f52c2f7510546542df7a42b719f09de413c90c789b54aee805bdd8aa16867  /work/lib/jnajack-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/dev/jna/jna/5.19.1/jna-5.19.1.jar -o /work/lib/jna-5.19.1.jar \
    && echo '4fb141dd8ef6b0585ffceea4bc49602fbc6312fa977e2c488794ea3e6aafecae  /work/lib/jna-5.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2.jar -o /work/lib/codecmedia-1.2.2.jar \
    && echo 'afa71e50c5f646d0f720aef4a5d31bc59b2f6c30858ba26feb5c2f180cc5f245  /work/lib/codecmedia-1.2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/psambit9791/jdsp/3.1.1/jdsp-3.1.1.jar -o /work/lib/jdsp-3.1.1.jar \
    && echo '6905c1131e0aeb00fadf013c4bfb5872eccf2a72be58a077aba6379bbfd7bcb7  /work/lib/jdsp-3.1.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/knowm/xchart/xchart/3.8.1/xchart-3.8.1.jar -o /work/lib/xchart-3.8.1.jar \
    && echo '610bb64d90bac7d2aeb25e7476d8b8df3d0f484315442dcab62685ff707c5ba5  /work/lib/xchart-3.8.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/erichseifert/vectorgraphics2d/VectorGraphics2D/0.13/VectorGraphics2D-0.13.jar -o /work/lib/VectorGraphics2D-0.13.jar \
    && echo '1b1c6248f1e70c52b8e9c09873350185aad081e70f83649ef85571ff269a71a2  /work/lib/VectorGraphics2D-0.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/rototor/pdfbox/graphics2d/0.32/graphics2d-0.32.jar -o /work/lib/graphics2d-0.32.jar \
    && echo '37f8f387395f96c214ac44f7475c7a2e1f832dfc1de289a3610e0ffbf728f679  /work/lib/graphics2d-0.32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox/2.0.24/pdfbox-2.0.24.jar -o /work/lib/pdfbox-2.0.24.jar \
    && echo '3c2c0553ec0e7533c490b4c952e1af113621de5275af6e380e11d0d9a0a4f3d6  /work/lib/pdfbox-2.0.24.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/fontbox/2.0.24/fontbox-2.0.24.jar -o /work/lib/fontbox-2.0.24.jar \
    && echo '2e8c0a569a90b04734fbc0c805d77f4ec03f98c11f5705055ccd7718c1953d68  /work/lib/fontbox-2.0.24.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar -o /work/lib/commons-logging-1.2.jar \
    && echo 'daddea1ea0be0f56978ab3006b8ac92834afeefbd9b7e4e6316fca57df0fa636  /work/lib/commons-logging-1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/madgag/animated-gif-lib/1.4/animated-gif-lib-1.4.jar -o /work/lib/animated-gif-lib-1.4.jar \
    && echo '49ad396efc16a076df137881e3a815922959bfb8d485e25f56bc3d3978c498cd  /work/lib/animated-gif-lib-1.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ca/umontreal/iro/simul/ssj/3.3.1/ssj-3.3.1.jar -o /work/lib/ssj-3.3.1.jar \
    && echo '39625d7ddef108b42307583a75346d36300cd64a5c11b944b1681d556fd0180d  /work/lib/ssj-3.3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jfree/jfreechart/1.0.12/jfreechart-1.0.12.jar -o /work/lib/jfreechart-1.0.12.jar \
    && echo 'b90e35874f89cf910c20214dce84c4906a09b908e4761ac32e248fe1b36102c3  /work/lib/jfreechart-1.0.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jfree/jcommon/1.0.15/jcommon-1.0.15.jar -o /work/lib/jcommon-1.0.15.jar \
    && echo 'acf524cbcd1ba61db2593b16b75a35fc1c7c58fd4d2d36e16ebb585d0f2cc509  /work/lib/jcommon-1.0.15.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/colt/colt/1.2.0/colt-1.2.0.jar -o /work/lib/colt-1.2.0.jar \
    && echo 'e1fcbfbdd0d0caedadfb59febace5a62812db3b9425f3a03ef4c4cbba3ed0ee3  /work/lib/colt-1.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/concurrent/concurrent/1.3.4/concurrent-1.3.4.jar -o /work/lib/concurrent-1.3.4.jar \
    && echo '12639def9a5b5ebf56040ab764bd42b7e662523d3b983e5d5da04bf37be152f9  /work/lib/concurrent-1.3.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/rwl/optimization/1.3/optimization-1.3.jar -o /work/lib/optimization-1.3.jar \
    && echo 'ecdf55d24cbf1ac4c48917f67de82178a128f4ae088de1611c8837acc4dd5f6d  /work/lib/optimization-1.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-math3/3.6.1/commons-math3-3.6.1.jar -o /work/lib/commons-math3-3.6.1.jar \
    && echo '1e56d7b058d28b65abd256b8458e3885b674c1d588fa43cd7d1cbb9c7ef2b308  /work/lib/commons-math3-3.6.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/uk/me/berndporr/iirj/1.5/iirj-1.5.jar -o /work/lib/iirj-1.5.jar \
    && echo '7260d395ce4fc54e96f2f2bbc6211a126a597ebeafb1f761b79895cf76a5f993  /work/lib/iirj-1.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0.jar -o /work/lib/tika-parser-audiovideo-module-4.2.0.jar \
    && echo '9c8d909e889a67a1a5c1a2db9353f08b8511038fa632f273c514f89c01900a4c  /work/lib/tika-parser-audiovideo-module-4.2.0.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openpreservation/jhove/jhove-modules/1.20.1/jhove-modules-1.20.1.jar -o /work/lib/jhove-modules-1.20.1.jar \
    && echo 'fbbc2769b72aeaa2f5cbf1c0df80798f1b1152ebef5c691741fb4a990e8156d3  /work/lib/jhove-modules-1.20.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openpreservation/jhove/jhove-core/1.20.1/jhove-core-1.20.1.jar -o /work/lib/jhove-core-1.20.1.jar \
    && echo '8540b65f595c5c42b85afeea51a10351f84930629c8f405d5acfdf9f5cd04c99  /work/lib/jhove-core-1.20.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/fracpete/musicg/1.4.2.2/musicg-1.4.2.2.jar -o /work/lib/musicg-1.4.2.2.jar \
    && echo 'aed1ba04957299d7c9fbdbca8bb38123f9680136bdf4f5890d7b6acd2e744795  /work/lib/musicg-1.4.2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.19.0/metadata-extractor-2.19.0.jar -o /work/lib/metadata-extractor-2.19.0.jar \
    && echo 'e51bb454ed08ea2bfcc3ad147d088ad1aa73a999e0072563f8ae50021a2fcadb  /work/lib/metadata-extractor-2.19.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/fracpete/musicg/1.4.2.2/musicg-1.4.2.2-sources.jar -o /work/parser-sources.jar \
    && echo '6a79536736c9edb651f2077640cc62df81d87e1f71bc45b058025310064d7ee4  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -qo /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY WavAdapter.java GenericHarness.java /work/src/
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
