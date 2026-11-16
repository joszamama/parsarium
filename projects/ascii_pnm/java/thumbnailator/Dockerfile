FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-imaging/1.0.0-alpha6/commons-imaging-1.0.0-alpha6.jar -o /work/lib/commons-imaging-1.0.0-alpha6.jar \
    && echo '19da061ae2d28d97dc0489a8735a48c2626168c462cd0c0a0bac87996921af5e  /work/lib/commons-imaging-1.0.0-alpha6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.19.0/commons-io-2.19.0.jar -o /work/lib/commons-io-2.19.0.jar \
    && echo '824268919b4b62f9f40f08c54381de5993b078f58667e332d17348ae019d72b9  /work/lib/commons-io-2.19.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.17.0/commons-lang3-3.17.0.jar -o /work/lib/commons-lang3-3.17.0.jar \
    && echo '6ee731df5c8e5a2976a1ca023b6bb320ea8d3539fbe64c8a1d5cb765127c33b4  /work/lib/commons-lang3-3.17.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-pnm/3.15.3/imageio-pnm-3.15.3.jar -o /work/lib/imageio-pnm-3.15.3.jar \
    && echo '4230e4fd6438de0d3f47b18dad88868865ae360c4fa77d4441bd637f6f6ac86e  /work/lib/imageio-pnm-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-core/3.15.3/imageio-core-3.15.3.jar -o /work/lib/imageio-core-3.15.3.jar \
    && echo '14d96b09384c48484b376127a0338f66875e94a67c99a3e94440a724bf1e0f09  /work/lib/imageio-core-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-lang/3.15.3/common-lang-3.15.3.jar -o /work/lib/common-lang-3.15.3.jar \
    && echo '24454ab8b23d8aaf54bb3a54e2187fdb5d96561905157852bdf75dddb730f426  /work/lib/common-lang-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-io/3.15.3/common-io-3.15.3.jar -o /work/lib/common-io-3.15.3.jar \
    && echo 'f5a164b4868ccef6baee5139d99b1b299fcc8f809dec882435b9a8fd61d473d3  /work/lib/common-io-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-image/3.15.3/common-image-3.15.3.jar -o /work/lib/common-image-3.15.3.jar \
    && echo '702f6edcbc91046c8a41c15d3a35e19aa3196536507169654370e3467e48c481  /work/lib/common-image-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/jai-imageio/jai-imageio-core/1.4.0/jai-imageio-core-1.4.0.jar -o /work/lib/jai-imageio-core-1.4.0.jar \
    && echo '8ad3c68e9efffb10ac87ff8bc589adf64b04a729c5194c079efd0643607fd72a  /work/lib/jai-imageio-core-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/imagej/ij/1.54p/ij-1.54p.jar -o /work/lib/ij-1.54p.jar \
    && echo '2e1a09961dfb41cee66ddc821b2577a41a072566ce45a49bae69267099741e20  /work/lib/ij-1.54p.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openpnp/opencv/4.9.0-0/opencv-4.9.0-0.jar -o /work/lib/opencv-4.9.0-0.jar \
    && echo '17823d249cb8ba18bc3cdb878db84936694d1cfaeac0f95517e320c8a8c458d9  /work/lib/opencv-4.9.0-0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/coobird/thumbnailator/0.4.21/thumbnailator-0.4.21.jar -o /work/lib/thumbnailator-0.4.21.jar \
    && echo '9ba7b5a55731932f2aec94e138b0f15166158e5881497dfb555db30836b7d607  /work/lib/thumbnailator-0.4.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-io/1.6.0/boofcv-io-1.6.0.jar -o /work/lib/boofcv-io-1.6.0.jar \
    && echo 'af381c255796a7edbe502fe397f8c2bbbaa7179c117966293123741d4e82c192  /work/lib/boofcv-io-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/georegression/georegression/0.30.2/georegression-0.30.2.jar -o /work/lib/georegression-0.30.2.jar \
    && echo 'd8d871555db282bbcbc6613e19e6113074280d7f8124b67445cca30da6feaeb0  /work/lib/georegression-0.30.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ddogleg/ddogleg/1.0.0/ddogleg-1.0.0.jar -o /work/lib/ddogleg-1.0.0.jar \
    && echo 'd7b89fefe0246a26e4876ebe2ad3362aa720fc2ccf150e135eba05520eb58fb9  /work/lib/ddogleg-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-core/0.46.1/ejml-core-0.46.1.jar -o /work/lib/ejml-core-0.46.1.jar \
    && echo '60e239ad8ad7b255542cab56986edec88f14feecdf86468b1ad37a7a7afe52e2  /work/lib/ejml-core-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-fdense/0.46.1/ejml-fdense-0.46.1.jar -o /work/lib/ejml-fdense-0.46.1.jar \
    && echo 'cfb01f81014f53cfb1def140b76150541123bfe886589d4b9043fc0d0125b688  /work/lib/ejml-fdense-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-ddense/0.46.1/ejml-ddense-0.46.1.jar -o /work/lib/ejml-ddense-0.46.1.jar \
    && echo '5e056bb27c1f39e612e8d05b3467bf1f05d0dc6c73f6b73a85fddf73127f901f  /work/lib/ejml-ddense-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-simple/0.46.1/ejml-simple-0.46.1.jar -o /work/lib/ejml-simple-0.46.1.jar \
    && echo '9f5dc17cde87c00570278aae3d9b2efcdd5b5e058728d6929ae892816c419f25  /work/lib/ejml-simple-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-cdense/0.46.1/ejml-cdense-0.46.1.jar -o /work/lib/ejml-cdense-0.46.1.jar \
    && echo 'bcae1ca55fc546b9f13e21042467281458f04b11d8e21015f248c6aebb9b2ab3  /work/lib/ejml-cdense-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-zdense/0.46.1/ejml-zdense-0.46.1.jar -o /work/lib/ejml-zdense-0.46.1.jar \
    && echo '6c0b124b7cdcec8387aa608f5e46304385ad0536dc7b790f5b0eab988c2e5dbc  /work/lib/ejml-zdense-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-fsparse/0.46.1/ejml-fsparse-0.46.1.jar -o /work/lib/ejml-fsparse-0.46.1.jar \
    && echo 'b834c5851ecdf65390af5cc487ef3167baf8ed4bd84463d42cc21591369b49aa  /work/lib/ejml-fsparse-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/ejml/ejml-dsparse/0.46.1/ejml-dsparse-0.46.1.jar -o /work/lib/ejml-dsparse-0.46.1.jar \
    && echo '3d3679e89895c5b9abc78ab7407c5b9218b247d38de5fa5ad8395c1b4d1ee30b  /work/lib/ejml-dsparse-0.46.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sf/trove4j/trove4j/3.0.3/trove4j-3.0.3.jar -o /work/lib/trove4j-3.0.3.jar \
    && echo '3c8616203d61a12a7e3487e8b34f3c198c2b5ba9e90da0c7ea32d99cd4958012  /work/lib/trove4j-3.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-ip/1.6.0/boofcv-ip-1.6.0.jar -o /work/lib/boofcv-ip-1.6.0.jar \
    && echo '6fa3cceb6aabd0eedb411600c1485428bde60f60c68404408df0d946fd5721c8  /work/lib/boofcv-ip-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-types/1.6.0/boofcv-types-1.6.0.jar -o /work/lib/boofcv-types-1.6.0.jar \
    && echo '3cc121687c4683177b45065f20a734b40087ca1e0a152056664c6e5708af6f36  /work/lib/boofcv-types-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-geo/1.6.0/boofcv-geo-1.6.0.jar -o /work/lib/boofcv-geo-1.6.0.jar \
    && echo '2f5cfe260e1b9258919409849e99f7137caa134e2ae0cf700333755daf7a3a19  /work/lib/boofcv-geo-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-sfm/1.6.0/boofcv-sfm-1.6.0.jar -o /work/lib/boofcv-sfm-1.6.0.jar \
    && echo '7e2a09b2e24464db6c1da1aab187e875b03aa8f3e367c8cd7f392adfbda754b0  /work/lib/boofcv-sfm-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-ip-multiview/1.6.0/boofcv-ip-multiview-1.6.0.jar -o /work/lib/boofcv-ip-multiview-1.6.0.jar \
    && echo 'e6ef6b972fef3a01692e2438bbc8e1323e2f269ca031cc4a00ba52405f028422  /work/lib/boofcv-ip-multiview-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-feature/1.6.0/boofcv-feature-1.6.0.jar -o /work/lib/boofcv-feature-1.6.0.jar \
    && echo 'bd3741db3c4e515257e70b5a80ee6dd94b642e1332aa778175b5ae2f0828ccea  /work/lib/boofcv-feature-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-recognition/1.6.0/boofcv-recognition-1.6.0.jar -o /work/lib/boofcv-recognition-1.6.0.jar \
    && echo 'e9f19b56ad9fdd34db24cd1e0670f373435780b089d8a74e9fbaa8b8de5e4146  /work/lib/boofcv-recognition-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/boofcv/boofcv-reconstruction/1.6.0/boofcv-reconstruction-1.6.0.jar -o /work/lib/boofcv-reconstruction-1.6.0.jar \
    && echo '090c9815eee7920bc37f91e4edd04e41c793528575d81e6a4ed1bc2886c340c5  /work/lib/boofcv-reconstruction-1.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/yaml/snakeyaml/2.3/snakeyaml-2.3.jar -o /work/lib/snakeyaml-2.3.jar \
    && echo '63a76fe66b652360bd4c2c107e6f0258daa7d4bb492008ba8c26fcd230ff9146  /work/lib/snakeyaml-2.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-image-module/4.2.0/tika-parser-image-module-4.2.0.jar -o /work/lib/tika-parser-image-module-4.2.0.jar \
    && echo 'd307ebcc4f472d0c00286101b891a722c05e3fdbd3dc3aa84776b7b70981839b  /work/lib/tika-parser-image-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0.jar -o /work/lib/metadata-extractor-2.22.0.jar \
    && echo 'af451be6b366b581d8deacccd1866a5264e6c7781fd2f46941811a1a2f7777f9  /work/lib/metadata-extractor-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/adobe/xmp/xmpcore/6.1.11/xmpcore-6.1.11.jar -o /work/lib/xmpcore-6.1.11.jar \
    && echo '8f7033c579b99fa0d9d6ddcb9448875b5e4b577c350002278ce46997d678b737  /work/lib/xmpcore-6.1.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-xmp-commons/4.2.0/tika-parser-xmp-commons-4.2.0.jar -o /work/lib/tika-parser-xmp-commons-4.2.0.jar \
    && echo '89860eadfb83934d1d6c7d1990e12568fc3d41028f4bf1c1310fe84b8da0413c  /work/lib/tika-parser-xmp-commons-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/jbig2-imageio/3.0.5/jbig2-imageio-3.0.5.jar -o /work/lib/jbig2-imageio-3.0.5.jar \
    && echo 'd426cc8b6ac211dd5ffd120a86a65e55ae65d808c818207c1261bc1880b42653  /work/lib/jbig2-imageio-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-core/4.2.0/tika-core-4.2.0.jar -o /work/lib/tika-core-4.2.0.jar \
    && echo '44f95d98ec7f6b48f3fa3fc816897ee822918dae32a9a944f9179c28dd678c86  /work/lib/tika-core-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.20/slf4j-api-2.0.20.jar -o /work/lib/slf4j-api-2.0.20.jar \
    && echo '7e1446499b359675d8aabe6af2de86b85e72ae8a2a932c0b40d0e5ba57097439  /work/lib/slf4j-api-2.0.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-secure-xml/1.1.0/commons-secure-xml-1.1.0.jar -o /work/lib/commons-secure-xml-1.1.0.jar \
    && echo '5fc54f0d153bb9c42379a434a05177e79bbfddec7791c383370da1f592789513  /work/lib/commons-secure-xml-1.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark/0.31.0/commonmark-0.31.0.jar -o /work/lib/commonmark-0.31.0.jar \
    && echo '11d5996813f4d6525a134b906844d87112c6acb6fdd306ad5755ef5df9b26281  /work/lib/commonmark-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-tables/0.31.0/commonmark-ext-gfm-tables-0.31.0.jar -o /work/lib/commonmark-ext-gfm-tables-0.31.0.jar \
    && echo 'd2b3e19fc2a55ca1274ef067c583b85abf8635f6dccd1f935cd36ffe8a186706  /work/lib/commonmark-ext-gfm-tables-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-strikethrough/0.31.0/commonmark-ext-gfm-strikethrough-0.31.0.jar -o /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar \
    && echo '6236e6605072708d0a172a9c57802529ab71958e71c72a5e0f90a4fbf62aa9aa  /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/coobird/thumbnailator/0.4.21/thumbnailator-0.4.21-sources.jar -o /work/parser-sources.jar \
    && echo '3fa9ddeae81e8b2f92f480c9d1cbb656b7dd58868e73181712b7f490e60593d8  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
RUN mkdir /work/parser-classes && javac -g:source,lines,vars -d /work/parser-classes $(find /work/parser-source/net -name '*.java')
COPY PnmAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
