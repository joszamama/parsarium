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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ar/com/hjg/pngj/2.1.0/pngj-2.1.0.jar -o /work/lib/pngj-2.1.0.jar \
    && echo 'e6b762f15e4891178dddd74e4d57318f518ce278000129efa41f85410b132ccc  /work/lib/pngj-2.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/coobird/thumbnailator/0.4.21/thumbnailator-0.4.21.jar -o /work/lib/thumbnailator-0.4.21.jar \
    && echo '9ba7b5a55731932f2aec94e138b0f15166158e5881497dfb555db30836b7d607  /work/lib/thumbnailator-0.4.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/imagej/ij/1.54p/ij-1.54p.jar -o /work/lib/ij-1.54p.jar \
    && echo '2e1a09961dfb41cee66ddc821b2577a41a072566ce45a49bae69267099741e20  /work/lib/ij-1.54p.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-codec/1.20/batik-codec-1.20.jar -o /work/lib/batik-codec-1.20.jar \
    && echo '9e5c979d85ec9e2b3c98d8acbfde627a22c5797c009f79998829e13f439eca39  /work/lib/batik-codec-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-awt-util/1.20/batik-awt-util-1.20.jar -o /work/lib/batik-awt-util-1.20.jar \
    && echo '3a98aa310e53756c16853f20ae9b9663388fe55714e0a9ba680900d72429a8ee  /work/lib/batik-awt-util-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-bridge/1.20/batik-bridge-1.20.jar -o /work/lib/batik-bridge-1.20.jar \
    && echo '199fca7f028ed3b39eb6a6016294876fd1de2b4b5ac6a17581b6697d8fdd598e  /work/lib/batik-bridge-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-anim/1.20/batik-anim-1.20.jar -o /work/lib/batik-anim-1.20.jar \
    && echo 'e221638a3e6a1f76a96c50ce0fdfb27341199e53385e9ad5dcfe935342a04141  /work/lib/batik-anim-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-ext/1.20/batik-ext-1.20.jar -o /work/lib/batik-ext-1.20.jar \
    && echo '59d909068ab88e6f4ab7285b63b21acd3c1632ee45846b2546a32f42b2963bcb  /work/lib/batik-ext-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-css/1.20/batik-css-1.20.jar -o /work/lib/batik-css-1.20.jar \
    && echo '65704f62745c1dc508a0ddeb33e4e2da397cd66f34375607b849c8ee898e4aee  /work/lib/batik-css-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.jar -o /work/lib/xml-apis-ext-1.3.04.jar \
    && echo 'd0b4887dc34d57de49074a58affad439a013d0baffa1a8034f8ef2a5ea191646  /work/lib/xml-apis-ext-1.3.04.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-dom/1.20/batik-dom-1.20.jar -o /work/lib/batik-dom-1.20.jar \
    && echo '6fae5082f9a722f7e336f2736a0faabacf1bafccd288984a8bafa6f35075e0ba  /work/lib/batik-dom-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-apis/xml-apis/1.4.01/xml-apis-1.4.01.jar -o /work/lib/xml-apis-1.4.01.jar \
    && echo 'a840968176645684bb01aed376e067ab39614885f9eee44abe35a5f20ebe7fad  /work/lib/xml-apis-1.4.01.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-gvt/1.20/batik-gvt-1.20.jar -o /work/lib/batik-gvt-1.20.jar \
    && echo '151232ae38c69533c3329b4a8cef2d8ab1f931f2b403ec15e5fa7eb6d4154e24  /work/lib/batik-gvt-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-parser/1.20/batik-parser-1.20.jar -o /work/lib/batik-parser-1.20.jar \
    && echo 'fff6626db0398d0842ffe5c24cab0475f289f00bbbad5f6859dc5b34dc3f2730  /work/lib/batik-parser-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-script/1.20/batik-script-1.20.jar -o /work/lib/batik-script-1.20.jar \
    && echo '6912cea4bff94e71239cc6d253a1731773bd218dd8e468c468b0246438293882  /work/lib/batik-script-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-svg-dom/1.20/batik-svg-dom-1.20.jar -o /work/lib/batik-svg-dom-1.20.jar \
    && echo 'a5c47749feb627ce4def49190e7c7286634ef04b0e5b4520b130ca62f3f13a9e  /work/lib/batik-svg-dom-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-xml/1.20/batik-xml-1.20.jar -o /work/lib/batik-xml-1.20.jar \
    && echo '2ce764d4d632c6ec147ac8f88c84eda0af1c3d6f6427927906ab8b1cbbb88da5  /work/lib/batik-xml-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-shared-resources/1.20/batik-shared-resources-1.20.jar -o /work/lib/batik-shared-resources-1.20.jar \
    && echo '24c8e3544b4c039c3742f1ddaf582e9fabba60c672731d5995de3c3dd62919c9  /work/lib/batik-shared-resources-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-transcoder/1.20/batik-transcoder-1.20.jar -o /work/lib/batik-transcoder-1.20.jar \
    && echo 'b1df7bacbd4f1ccb0419acf7aa3b1902c60b4d0ec00534425145a47907280a35  /work/lib/batik-transcoder-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-svggen/1.20/batik-svggen-1.20.jar -o /work/lib/batik-svggen-1.20.jar \
    && echo 'fa0ce75dcf4c682ad2a347b9d2767263e58d0cc4e6c1961b1e55b0e413a9a875  /work/lib/batik-svggen-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-util/1.20/batik-util-1.20.jar -o /work/lib/batik-util-1.20.jar \
    && echo '4cd87c956d6f522ebb67fd165252f8391e8c184c50559f7d7dc3ff95cc491e3c  /work/lib/batik-util-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-constants/1.20/batik-constants-1.20.jar -o /work/lib/batik-constants-1.20.jar \
    && echo 'b853b0ce2a7ce235eebf5197bd15ca40bf9c7ffc9a698e382fd47ce7c36e258e  /work/lib/batik-constants-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-i18n/1.20/batik-i18n-1.20.jar -o /work/lib/batik-i18n-1.20.jar \
    && echo '9030abd0720d3bbab46b0af27f8867f1919dc74cabe8255ae9865e79b288ba5e  /work/lib/batik-i18n-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/depsypher/pngtastic/1.8/pngtastic-1.8.jar -o /work/lib/pngtastic-1.8.jar \
    && echo '4f4865d28368344feefbec0c5784a4d4f1044fbf5bcf24c5f7b40e1d0e384b93  /work/lib/pngtastic-1.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/itextpdf/5.5.13/itextpdf-5.5.13.jar -o /work/lib/itextpdf-5.5.13.jar \
    && echo '368500a5f57fd0b04e565e78cfe469e61c362e86445667a29c9645dd2ce10b3d  /work/lib/itextpdf-5.5.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0.jar -o /work/lib/metadata-extractor-2.22.0.jar \
    && echo 'af451be6b366b581d8deacccd1866a5264e6c7781fd2f46941811a1a2f7777f9  /work/lib/metadata-extractor-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/adobe/xmp/xmpcore/6.1.11/xmpcore-6.1.11.jar -o /work/lib/xmpcore-6.1.11.jar \
    && echo '8f7033c579b99fa0d9d6ddcb9448875b5e4b577c350002278ce46997d678b737  /work/lib/xmpcore-6.1.11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jopendocument/jOpenDocument/1.3/jOpenDocument-1.3.jar -o /work/lib/jOpenDocument-1.3.jar \
    && echo '25cbb135beccc564c24701bd5feea28b4a032a7015f42d6d05a9333d8517daeb  /work/lib/jOpenDocument-1.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox/3.0.8/pdfbox-3.0.8.jar -o /work/lib/pdfbox-3.0.8.jar \
    && echo '97647cfbde61ebcfc06b4cf8c9b0ffcaaee073396eceb4a7f6836a9b9128903c  /work/lib/pdfbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox-io/3.0.8/pdfbox-io-3.0.8.jar -o /work/lib/pdfbox-io-3.0.8.jar \
    && echo '36a0e04001010b4c764857817412b96339930b19755e728959805cc0352061b2  /work/lib/pdfbox-io-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/fontbox/3.0.8/fontbox-3.0.8.jar -o /work/lib/fontbox-3.0.8.jar \
    && echo 'a1915c24e3edbe0ecec93896dfbf6d41427810b663ade97bd4e8bae86ec3fdab  /work/lib/fontbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.4.0/commons-logging-1.4.0.jar -o /work/lib/commons-logging-1.4.0.jar \
    && echo 'd175dbd751dd782a63bde28c7a039520e971f25e84b79c19b8435edc3603e0dc  /work/lib/commons-logging-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec-javase/0.2.5/jcodec-javase-0.2.5.jar -o /work/lib/jcodec-javase-0.2.5.jar \
    && echo '8a72ff7560bce1c89c1d815816d1304383bb4048afeeb91f200b7a1e213ab6ae  /work/lib/jcodec-javase-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.jar -o /work/lib/jcodec-0.2.5.jar \
    && echo '890329dad124e8b739c1d6602a59a53c8a474daddff265c2561e21c498496c81  /work/lib/jcodec-0.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/librepdf/openpdf/3.0.5/openpdf-3.0.5.jar -o /work/lib/openpdf-3.0.5.jar \
    && echo '2a70c6024bb10b6192b4b91d8bb581de24b776a799a30ef5b87748e54aca2144  /work/lib/openpdf-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/brotli4j/1.23.0/brotli4j-1.23.0.jar -o /work/lib/brotli4j-1.23.0.jar \
    && echo '5fcf13ad78d07319cc507465dcf61cbc3efee9f45c9ae1c42a9902414696bc0b  /work/lib/brotli4j-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/service/1.23.0/service-1.23.0.jar -o /work/lib/service-1.23.0.jar \
    && echo '7f298d44dbb7688419f0179ee1dfa0e4436633272b05d38a5faf3a2b8d08697b  /work/lib/service-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/native-osx-aarch64/1.23.0/native-osx-aarch64-1.23.0.jar -o /work/lib/native-osx-aarch64-1.23.0.jar \
    && echo 'be3bc53688dbaff26d9d554301837de2bfa9ec09090b64d1ebf1fb6b23c28e61  /work/lib/native-osx-aarch64-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/io/9.8.0/io-9.8.0.jar -o /work/lib/io-9.8.0.jar \
    && echo '90c2a19aff026e7157b0500835cc321a0679f76dd2e865e3dbd5c8e07dc36a5c  /work/lib/io-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/commons/9.8.0/commons-9.8.0.jar -o /work/lib/commons-9.8.0.jar \
    && echo 'f650e713ed571bfb0fedbf44fe38e947d21aa77b10c94fea95effc98370d8279  /work/lib/commons-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.22.3/jackson-databind-2.22.3.jar -o /work/lib/jackson-databind-2.22.3.jar \
    && echo '556db5439e206114346043f68d200497dc96a0bca62a360a81784092ebd0e0a9  /work/lib/jackson-databind-2.22.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.22/jackson-annotations-2.22.jar -o /work/lib/jackson-annotations-2.22.jar \
    && echo '21ddb598807d3a51a876704eb979d9296e1c6a6f47ab1826ff88c6d6a127a2d0  /work/lib/jackson-annotations-2.22.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/fasterxml/jackson/core/jackson-core/2.22.3/jackson-core-2.22.3.jar -o /work/lib/jackson-core-2.22.3.jar \
    && echo '8a501126a385b25841915d839508f8a66e2a0dbc8a6709d055ef3b3e852b094c  /work/lib/jackson-core-2.22.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.16/slf4j-api-2.0.16.jar -o /work/lib/slf4j-api-2.0.16.jar \
    && echo 'a12578dde1ba00bd9b816d388a0b879928d00bab3c83c240f7013bf4196c579a  /work/lib/slf4j-api-2.0.16.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-stb/3.4.3/lwjgl-stb-3.4.3.jar -o /work/lib/lwjgl-stb-3.4.3.jar \
    && echo '544753f5e49c53580949b9f1fc341f0e434991303c93d5a428fbaafaacc2cd69  /work/lib/lwjgl-stb-3.4.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.4.3/lwjgl-3.4.3.jar -o /work/lib/lwjgl-3.4.3.jar \
    && echo '46eeca5471833c3cf5da3c1da015b41e3bb3eb16dd3da03f366886da10096751  /work/lib/lwjgl-3.4.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-stb/3.4.3/lwjgl-stb-3.4.3-natives-macos-arm64.jar -o /work/lib/lwjgl-stb-3.4.3-natives-macos-arm64.jar \
    && echo 'c038b8f586214fe762eb0876890103ffc77869c96c94572f13b1428b384df034  /work/lib/lwjgl-stb-3.4.3-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.4.3/lwjgl-3.4.3-natives-macos-arm64.jar -o /work/lib/lwjgl-3.4.3-natives-macos-arm64.jar \
    && echo '0cf1eac3c360395846320ec47a5e0da313fbb5ee92414ce09ba7e7cc11274509  /work/lib/lwjgl-3.4.3-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-image-module/4.2.0/tika-parser-image-module-4.2.0.jar -o /work/lib/tika-parser-image-module-4.2.0.jar \
    && echo 'd307ebcc4f472d0c00286101b891a722c05e3fdbd3dc3aa84776b7b70981839b  /work/lib/tika-parser-image-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-xmp-commons/4.2.0/tika-parser-xmp-commons-4.2.0.jar -o /work/lib/tika-parser-xmp-commons-4.2.0.jar \
    && echo '89860eadfb83934d1d6c7d1990e12568fc3d41028f4bf1c1310fe84b8da0413c  /work/lib/tika-parser-xmp-commons-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/jai-imageio/jai-imageio-core/1.4.0/jai-imageio-core-1.4.0.jar -o /work/lib/jai-imageio-core-1.4.0.jar \
    && echo '8ad3c68e9efffb10ac87ff8bc589adf64b04a729c5194c079efd0643607fd72a  /work/lib/jai-imageio-core-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/jbig2-imageio/3.0.5/jbig2-imageio-3.0.5.jar -o /work/lib/jbig2-imageio-3.0.5.jar \
    && echo 'd426cc8b6ac211dd5ffd120a86a65e55ae65d808c818207c1261bc1880b42653  /work/lib/jbig2-imageio-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-core/4.2.0/tika-core-4.2.0.jar -o /work/lib/tika-core-4.2.0.jar \
    && echo '44f95d98ec7f6b48f3fa3fc816897ee822918dae32a9a944f9179c28dd678c86  /work/lib/tika-core-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-secure-xml/1.1.0/commons-secure-xml-1.1.0.jar -o /work/lib/commons-secure-xml-1.1.0.jar \
    && echo '5fc54f0d153bb9c42379a434a05177e79bbfddec7791c383370da1f592789513  /work/lib/commons-secure-xml-1.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark/0.31.0/commonmark-0.31.0.jar -o /work/lib/commonmark-0.31.0.jar \
    && echo '11d5996813f4d6525a134b906844d87112c6acb6fdd306ad5755ef5df9b26281  /work/lib/commonmark-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-tables/0.31.0/commonmark-ext-gfm-tables-0.31.0.jar -o /work/lib/commonmark-ext-gfm-tables-0.31.0.jar \
    && echo 'd2b3e19fc2a55ca1274ef067c583b85abf8635f6dccd1f935cd36ffe8a186706  /work/lib/commonmark-ext-gfm-tables-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/commonmark/commonmark-ext-gfm-strikethrough/0.31.0/commonmark-ext-gfm-strikethrough-0.31.0.jar -o /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar \
    && echo '6236e6605072708d0a172a9c57802529ab71958e71c72a5e0f90a4fbf62aa9aa  /work/lib/commonmark-ext-gfm-strikethrough-0.31.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/xmlgraphics-commons/2.12/xmlgraphics-commons-2.12.jar -o /work/lib/xmlgraphics-commons-2.12.jar \
    && echo '85be03f2f47e08007130db9efbcc587afd3ae08dd13c704ecf472dd88867e061  /work/lib/xmlgraphics-commons-2.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-graphics/21.0.9/javafx-graphics-21.0.9-mac-aarch64.jar -o /work/lib/javafx-graphics-21.0.9-mac-aarch64.jar \
    && echo 'e78affd7b4b2c3704716fa4097a7427152e23de353e384618ca87747068646df  /work/lib/javafx-graphics-21.0.9-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-base/21.0.9/javafx-base-21.0.9.jar -o /work/lib/javafx-base-21.0.9.jar \
    && echo '31bcb252641eed1fdfc6a89d361ad75532a02af8fea198fd3bc48b5ec128c1b0  /work/lib/javafx-base-21.0.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-base/21.0.9/javafx-base-21.0.9-mac-aarch64.jar -o /work/lib/javafx-base-21.0.9-mac-aarch64.jar \
    && echo 'eb41a8159be86e3e76ee0f2e18b2bce85e8613da3188fdce13527a7dda644222  /work/lib/javafx-base-21.0.9-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openpnp/opencv/4.9.0-0/opencv-4.9.0-0.jar -o /work/lib/opencv-4.9.0-0.jar \
    && echo '17823d249cb8ba18bc3cdb878db84936694d1cfaeac0f95517e320c8a8c458d9  /work/lib/opencv-4.9.0-0.jar' | sha256sum --check
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
COPY PngAdapter.java GenericHarness.java /work/src/
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
