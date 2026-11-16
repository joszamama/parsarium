FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-transcoder/1.20/batik-transcoder-1.20.jar -o /work/lib/batik-transcoder-1.20.jar \
    && echo 'b1df7bacbd4f1ccb0419acf7aa3b1902c60b4d0ec00534425145a47907280a35  /work/lib/batik-transcoder-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-awt-util/1.20/batik-awt-util-1.20.jar -o /work/lib/batik-awt-util-1.20.jar \
    && echo '3a98aa310e53756c16853f20ae9b9663388fe55714e0a9ba680900d72429a8ee  /work/lib/batik-awt-util-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-bridge/1.20/batik-bridge-1.20.jar -o /work/lib/batik-bridge-1.20.jar \
    && echo '199fca7f028ed3b39eb6a6016294876fd1de2b4b5ac6a17581b6697d8fdd598e  /work/lib/batik-bridge-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-dom/1.20/batik-dom-1.20.jar -o /work/lib/batik-dom-1.20.jar \
    && echo '6fae5082f9a722f7e336f2736a0faabacf1bafccd288984a8bafa6f35075e0ba  /work/lib/batik-dom-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-apis/xml-apis/1.4.01/xml-apis-1.4.01.jar -o /work/lib/xml-apis-1.4.01.jar \
    && echo 'a840968176645684bb01aed376e067ab39614885f9eee44abe35a5f20ebe7fad  /work/lib/xml-apis-1.4.01.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-gvt/1.20/batik-gvt-1.20.jar -o /work/lib/batik-gvt-1.20.jar \
    && echo '151232ae38c69533c3329b4a8cef2d8ab1f931f2b403ec15e5fa7eb6d4154e24  /work/lib/batik-gvt-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-shared-resources/1.20/batik-shared-resources-1.20.jar -o /work/lib/batik-shared-resources-1.20.jar \
    && echo '24c8e3544b4c039c3742f1ddaf582e9fabba60c672731d5995de3c3dd62919c9  /work/lib/batik-shared-resources-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-svggen/1.20/batik-svggen-1.20.jar -o /work/lib/batik-svggen-1.20.jar \
    && echo 'fa0ce75dcf4c682ad2a347b9d2767263e58d0cc4e6c1961b1e55b0e413a9a875  /work/lib/batik-svggen-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-util/1.20/batik-util-1.20.jar -o /work/lib/batik-util-1.20.jar \
    && echo '4cd87c956d6f522ebb67fd165252f8391e8c184c50559f7d7dc3ff95cc491e3c  /work/lib/batik-util-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-constants/1.20/batik-constants-1.20.jar -o /work/lib/batik-constants-1.20.jar \
    && echo 'b853b0ce2a7ce235eebf5197bd15ca40bf9c7ffc9a698e382fd47ce7c36e258e  /work/lib/batik-constants-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-i18n/1.20/batik-i18n-1.20.jar -o /work/lib/batik-i18n-1.20.jar \
    && echo '9030abd0720d3bbab46b0af27f8867f1919dc74cabe8255ae9865e79b288ba5e  /work/lib/batik-i18n-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-xml/1.20/batik-xml-1.20.jar -o /work/lib/batik-xml-1.20.jar \
    && echo '2ce764d4d632c6ec147ac8f88c84eda0af1c3d6f6427927906ab8b1cbbb88da5  /work/lib/batik-xml-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-codec/1.20/batik-codec-1.20.jar -o /work/lib/batik-codec-1.20.jar \
    && echo '9e5c979d85ec9e2b3c98d8acbfde627a22c5797c009f79998829e13f439eca39  /work/lib/batik-codec-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-anim/1.20/batik-anim-1.20.jar -o /work/lib/batik-anim-1.20.jar \
    && echo 'e221638a3e6a1f76a96c50ce0fdfb27341199e53385e9ad5dcfe935342a04141  /work/lib/batik-anim-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-css/1.20/batik-css-1.20.jar -o /work/lib/batik-css-1.20.jar \
    && echo '65704f62745c1dc508a0ddeb33e4e2da397cd66f34375607b849c8ee898e4aee  /work/lib/batik-css-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.jar -o /work/lib/xml-apis-ext-1.3.04.jar \
    && echo 'd0b4887dc34d57de49074a58affad439a013d0baffa1a8034f8ef2a5ea191646  /work/lib/xml-apis-ext-1.3.04.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-ext/1.20/batik-ext-1.20.jar -o /work/lib/batik-ext-1.20.jar \
    && echo '59d909068ab88e6f4ab7285b63b21acd3c1632ee45846b2546a32f42b2963bcb  /work/lib/batik-ext-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-parser/1.20/batik-parser-1.20.jar -o /work/lib/batik-parser-1.20.jar \
    && echo 'fff6626db0398d0842ffe5c24cab0475f289f00bbbad5f6859dc5b34dc3f2730  /work/lib/batik-parser-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-svg-dom/1.20/batik-svg-dom-1.20.jar -o /work/lib/batik-svg-dom-1.20.jar \
    && echo 'a5c47749feb627ce4def49190e7c7286634ef04b0e5b4520b130ca62f3f13a9e  /work/lib/batik-svg-dom-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-svgrasterizer/1.20/batik-svgrasterizer-1.20.jar -o /work/lib/batik-svgrasterizer-1.20.jar \
    && echo '37636b6bfa3f64d1622291088ae49d3883c15ef276d606dc824ecaf4b78e58f1  /work/lib/batik-svgrasterizer-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-swing/1.20/batik-swing-1.20.jar -o /work/lib/batik-swing-1.20.jar \
    && echo 'a79040e77111e83d3e5788230b2ecffa7421b5cf843763d87ea86b1b8acee87f  /work/lib/batik-swing-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-gui-util/1.20/batik-gui-util-1.20.jar -o /work/lib/batik-gui-util-1.20.jar \
    && echo 'c65f15d606414844616002f92917aece2f9e446e0cd39e541d7088035ed3e859  /work/lib/batik-gui-util-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-script/1.20/batik-script-1.20.jar -o /work/lib/batik-script-1.20.jar \
    && echo '6912cea4bff94e71239cc6d253a1731773bd218dd8e468c468b0246438293882  /work/lib/batik-script-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/svg/9.8.0/svg-9.8.0.jar -o /work/lib/svg-9.8.0.jar \
    && echo '949a6974ebc812d589cf01bd9e11235ed1603b841afa0eaf14999bde6ecddf87  /work/lib/svg-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/layout/9.8.0/layout-9.8.0.jar -o /work/lib/layout-9.8.0.jar \
    && echo '0a44d2f73dc2065c5c2107f146561122856c5e8f01751e9994cef7d927c25848  /work/lib/layout-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/kernel/9.8.0/kernel-9.8.0.jar -o /work/lib/kernel-9.8.0.jar \
    && echo 'f0e4ae6ba1fc52e9332aa827206e4848ddc0fb69fb138988d9760462d75a0877  /work/lib/kernel-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/bouncy-castle-connector/9.8.0/bouncy-castle-connector-9.8.0.jar -o /work/lib/bouncy-castle-connector-9.8.0.jar \
    && echo '04b0eaf8de7244c06f284c67c765e5f91c6edb34098c853affcc3a30b9165163  /work/lib/bouncy-castle-connector-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/styled-xml-parser/9.8.0/styled-xml-parser-9.8.0.jar -o /work/lib/styled-xml-parser-9.8.0.jar \
    && echo '47c6fb54b58f9a1575684611b025f25b92de8c7c6e9fca73a00a97c5e6bce0a4  /work/lib/styled-xml-parser-9.8.0.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/fop-core/2.12/fop-core-2.12.jar -o /work/lib/fop-core-2.12.jar \
    && echo '527dc27e554110ec3528815ee21e85b28a7721e8198ad48795d00fe0031e5f9b  /work/lib/fop-core-2.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-extension/1.20/batik-extension-1.20.jar -o /work/lib/batik-extension-1.20.jar \
    && echo 'd0751492aab9e3d8baea85a8cca599d39d933d0ca1fde86b6fd2d393c1f530b7  /work/lib/batik-extension-1.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/fop-events/2.12/fop-events-2.12.jar -o /work/lib/fop-events-2.12.jar \
    && echo 'f9674631515863c6e85572e687542f0201a8092a83a6f6ba3633a45022e59029  /work/lib/fop-events-2.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/fop-util/2.12/fop-util-2.12.jar -o /work/lib/fop-util-2.12.jar \
    && echo 'cacfd834fda3e9f8af6d12b0b35d5b4175e3e1929595d1f8169a86b1042c1791  /work/lib/fop-util-2.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/xmlgraphics-commons/2.12/xmlgraphics-commons-2.12.jar -o /work/lib/xmlgraphics-commons-2.12.jar \
    && echo '85be03f2f47e08007130db9efbcc587afd3ae08dd13c704ecf472dd88867e061  /work/lib/xmlgraphics-commons-2.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.17.0/commons-io-2.17.0.jar -o /work/lib/commons-io-2.17.0.jar \
    && echo '4aa4ca48f3dfd30b78220b7881d8cb93eac4093ec94361b6befa9487998a550b  /work/lib/commons-io-2.17.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.3.0/commons-logging-1.3.0.jar -o /work/lib/commons-logging-1.3.0.jar \
    && echo '66d3c980470b99b0c511dad3dfc0ae7b265ec1fb144e96bc0253a8a175fd34d9  /work/lib/commons-logging-1.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/fontbox/3.0.3/fontbox-3.0.3.jar -o /work/lib/fontbox-3.0.3.jar \
    && echo '65690c3f39b04a14d12c17f4998c15186ce877d3e2ec222c708577e3cc028030  /work/lib/fontbox-3.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox-io/3.0.3/pdfbox-io-3.0.3.jar -o /work/lib/pdfbox-io-3.0.3.jar \
    && echo '123ea3187b497c54e661d50c3c867479bf77668ff450e50710c658f2bb4687ba  /work/lib/pdfbox-io-3.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/pushing-pixels/radiance-svg-transcoder/7.5.0/radiance-svg-transcoder-7.5.0.jar -o /work/lib/radiance-svg-transcoder-7.5.0.jar \
    && echo '2838df85b30fe3b3343bc4f82bf67226a566c261592bbe6d1c7bef3f201c3b7a  /work/lib/radiance-svg-transcoder-7.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlgraphics/batik-all/1.17/batik-all-1.17.jar -o /work/lib/batik-all-1.17.jar \
    && echo '174b616d93ea4dab9a6d0c23c1ab5f146123c0ee2534087931607f9ee1253191  /work/lib/batik-all-1.17.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/pushing-pixels/radiance-common/7.5.0/radiance-common-7.5.0.jar -o /work/lib/radiance-common-7.5.0.jar \
    && echo 'd272bf8648e8b3dcc85bd191392507e3f94990de001d63103dd28afdee58ada0  /work/lib/radiance-common-7.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/pushing-pixels/aurora-tools-svg-transcoder-desktop/1.3.0/aurora-tools-svg-transcoder-desktop-1.3.0.jar -o /work/lib/aurora-tools-svg-transcoder-desktop-1.3.0.jar \
    && echo 'f7e51bdd39add60b26d616796d11748ac636b54d7a035ea6b598632d9491de5c  /work/lib/aurora-tools-svg-transcoder-desktop-1.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/desktop/desktop-jvm/1.2.1/desktop-jvm-1.2.1.jar -o /work/lib/desktop-jvm-1.2.1.jar \
    && echo '8248b892fa3c16e3fb76d394f6b8ba72efae5e42910530f8eb1d2cb2cf38507b  /work/lib/desktop-jvm-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/foundation/foundation-desktop/1.2.1/foundation-desktop-1.2.1.jar -o /work/lib/foundation-desktop-1.2.1.jar \
    && echo '997534020ec2f7526f378e61e5e9bf3a7144fa19e2d0ac89fd62627fbd40dffb  /work/lib/foundation-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/animation/animation-desktop/1.2.1/animation-desktop-1.2.1.jar -o /work/lib/animation-desktop-1.2.1.jar \
    && echo 'fd928926c2a4ba271ff10e0537ac42b398554fc5be041b96289d076ab8a022b1  /work/lib/animation-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/foundation/foundation-layout-desktop/1.2.1/foundation-layout-desktop-1.2.1.jar -o /work/lib/foundation-layout-desktop-1.2.1.jar \
    && echo 'b38aa3f80c2628ad70c00adb1e27d3569865755e9de22cd253f7ea0bea6129e0  /work/lib/foundation-layout-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-text-desktop/1.2.1/ui-text-desktop-1.2.1.jar -o /work/lib/ui-text-desktop-1.2.1.jar \
    && echo 'e91229871dd13787e3819e7a29608cdd3c15bb61184525bdb95bf5b71b46cf05  /work/lib/ui-text-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/skiko/skiko-awt/0.7.37/skiko-awt-0.7.37.jar -o /work/lib/skiko-awt-0.7.37.jar \
    && echo 'e345f313d2e1627c6bd6e93981dc8c6058febd6269d13b93ea99384177ccbf23  /work/lib/skiko-awt-0.7.37.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/material/material-desktop/1.2.1/material-desktop-1.2.1.jar -o /work/lib/material-desktop-1.2.1.jar \
    && echo 'a747d310c35313df5cac796403edc11eb4baa467fb0a614eb1ef123152bf1262  /work/lib/material-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/animation/animation-core-desktop/1.2.1/animation-core-desktop-1.2.1.jar -o /work/lib/animation-core-desktop-1.2.1.jar \
    && echo 'f0c3a21f83eee5aaaef7566b9c9301f2ddcd34d1276c6d312a15a042879d0024  /work/lib/animation-core-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/material/material-icons-core-desktop/1.2.1/material-icons-core-desktop-1.2.1.jar -o /work/lib/material-icons-core-desktop-1.2.1.jar \
    && echo 'fa400014102b141d277ce8b0ae1d35943e7f83ac7a52a1865290b1f5fca77332  /work/lib/material-icons-core-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/material/material-ripple-desktop/1.2.1/material-ripple-desktop-1.2.1.jar -o /work/lib/material-ripple-desktop-1.2.1.jar \
    && echo 'e6eb0a2986cf45dd1a04a374ef6f4fecb0ea3522f7125d6c3c17fd26904e3c1b  /work/lib/material-ripple-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/runtime/runtime-desktop/1.2.1/runtime-desktop-1.2.1.jar -o /work/lib/runtime-desktop-1.2.1.jar \
    && echo '3d42c85ce83631f503bf242533a1f46c7face1a7021fe76c7371fbbabcfae94d  /work/lib/runtime-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/atomicfu-jvm/0.17.2/atomicfu-jvm-0.17.2.jar -o /work/lib/atomicfu-jvm-0.17.2.jar \
    && echo '636968b47a6c31262ebc984255e56ca54a8dd16de7f17c35103aac88d827256e  /work/lib/atomicfu-jvm-0.17.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-desktop/1.2.1/ui-desktop-1.2.1.jar -o /work/lib/ui-desktop-1.2.1.jar \
    && echo 'e78bb9f76610a5bdc0e0f5349fefb9a592b1b6b54efb18757900d5edd67ed547  /work/lib/ui-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/runtime/runtime-saveable-desktop/1.2.1/runtime-saveable-desktop-1.2.1.jar -o /work/lib/runtime-saveable-desktop-1.2.1.jar \
    && echo 'f0b1a2d7fb6ca14639ab329bc0d9d70eb5896bc8719340efd1611409cadc3fb6  /work/lib/runtime-saveable-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-geometry-desktop/1.2.1/ui-geometry-desktop-1.2.1.jar -o /work/lib/ui-geometry-desktop-1.2.1.jar \
    && echo 'eafb98efa790aa0a9621e8db9b6150be091e1f377cab4346fa86aa1f0f6d552c  /work/lib/ui-geometry-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-graphics-desktop/1.2.1/ui-graphics-desktop-1.2.1.jar -o /work/lib/ui-graphics-desktop-1.2.1.jar \
    && echo 'a5573c7f19b5501c53ec532595b2149b6568624004778a90a0ebd5800f3edca6  /work/lib/ui-graphics-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-unit-desktop/1.2.1/ui-unit-desktop-1.2.1.jar -o /work/lib/ui-unit-desktop-1.2.1.jar \
    && echo 'b9a82caf4188544fc8f9ccf120f2dd8003571e2147150165c6a74c00fcba63c8  /work/lib/ui-unit-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-tooling-preview-desktop/1.2.1/ui-tooling-preview-desktop-1.2.1.jar -o /work/lib/ui-tooling-preview-desktop-1.2.1.jar \
    && echo 'db49ff56acf0a3c0f3062ed744c0cd3498dedf8a2785fe91cc6d6a64bfd4b99a  /work/lib/ui-tooling-preview-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/compose/ui/ui-util-desktop/1.2.1/ui-util-desktop-1.2.1.jar -o /work/lib/ui-util-desktop-1.2.1.jar \
    && echo '518a6042ef106536b8f77d8127f2ea7b7b9434b76809703e61f7eedc8835cd29  /work/lib/ui-util-desktop-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.6.21/kotlin-stdlib-1.6.21.jar -o /work/lib/kotlin-stdlib-1.6.21.jar \
    && echo '739c526672bb337573b28f63afa8306eb088b0c3a0967f56d6c89f4a3012a492  /work/lib/kotlin-stdlib-1.6.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar -o /work/lib/annotations-13.0.jar \
    && echo 'ace2a10dc8e2d5fd34925ecac03e4988b2c0f851650c94b8cef49ba1bd111478  /work/lib/annotations-13.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-common/1.6.21/kotlin-stdlib-common-1.6.21.jar -o /work/lib/kotlin-stdlib-common-1.6.21.jar \
    && echo '183bec59cd9f3a14957b190e8c879cf1194bd1f106b0a7b6e1cbb8790d242363  /work/lib/kotlin-stdlib-common-1.6.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-coroutines-core/1.6.1/kotlinx-coroutines-core-1.6.1.jar -o /work/lib/kotlinx-coroutines-core-1.6.1.jar \
    && echo '675489984c662362f48f48789a2cb9c2a711d515f3935d8f37b612790ad1e417  /work/lib/kotlinx-coroutines-core-1.6.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-coroutines-core-jvm/1.6.1/kotlinx-coroutines-core-jvm-1.6.1.jar -o /work/lib/kotlinx-coroutines-core-jvm-1.6.1.jar \
    && echo '3a93ffd052844643c0fef950ae5578db47cccbe9e7176d681333182e232bb0f1  /work/lib/kotlinx-coroutines-core-jvm-1.6.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk8/1.7.20/kotlin-stdlib-jdk8-1.7.20.jar -o /work/lib/kotlin-stdlib-jdk8-1.7.20.jar \
    && echo '1da0d306c995945e1f807240ef64b5cd2dd5ac58612afb1a8596143d10b7ded5  /work/lib/kotlin-stdlib-jdk8-1.7.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk7/1.7.20/kotlin-stdlib-jdk7-1.7.20.jar -o /work/lib/kotlin-stdlib-jdk7-1.7.20.jar \
    && echo '524da3c1a2ad56fd52c4ae2272ef3de421de8d2047ab1c51fc306d351243f2f5  /work/lib/kotlin-stdlib-jdk7-1.7.20.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/se/alipsa/groovy/gsvg/1.2.0/gsvg-1.2.0.jar -o /work/lib/gsvg-1.2.0.jar \
    && echo '21089a24d906f47b644e69105b8a269436394b538411d2523a2a6b1c43b52a82  /work/lib/gsvg-1.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/dom4j/dom4j/2.2.0/dom4j-2.2.0.jar -o /work/lib/dom4j-2.2.0.jar \
    && echo '3fae79e081096e1410645eb3557c63b79ca266d510ab479889511109becd1690  /work/lib/dom4j-2.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jaxen/jaxen/2.0.6/jaxen-2.0.6.jar -o /work/lib/jaxen-2.0.6.jar \
    && echo '3e2a755b283fd492fa4be204294c7abb7cd63ac94fb366baab9c7bb9afb00b6d  /work/lib/jaxen-2.0.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/ph-css/8.2.1/ph-css-8.2.1.jar -o /work/lib/ph-css-8.2.1.jar \
    && echo '0a0f85a41c05ea96f2c9713bb08e4d4bbbb13dbb92bcf2a734003429659d5686  /work/lib/ph-css-8.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-typeconvert/12.2.5/ph-typeconvert-12.2.5.jar -o /work/lib/ph-typeconvert-12.2.5.jar \
    && echo 'f489f95dcae67af051719bb23a2769fd4ba44bf07c53932bd01174008a8b4397  /work/lib/ph-typeconvert-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-collection/12.2.5/ph-collection-12.2.5.jar -o /work/lib/ph-collection-12.2.5.jar \
    && echo 'a1f70946f0ea112574d9eccc22a2b46696c44ca17be772eb7782d9b1b09d19fa  /work/lib/ph-collection-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-base/12.2.5/ph-base-12.2.5.jar -o /work/lib/ph-base-12.2.5.jar \
    && echo 'd516b4e040aa05853202ce653fb5b426d3c8d24f81eed6970ca93a2eefe29cc7  /work/lib/ph-base-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-cache/12.2.5/ph-cache-12.2.5.jar -o /work/lib/ph-cache-12.2.5.jar \
    && echo 'b930d2ff3fad52a5f75e8fc65c2012fabb9a11098189d4c72cf192bea50f610a  /work/lib/ph-cache-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-annotations/12.2.5/ph-annotations-12.2.5.jar -o /work/lib/ph-annotations-12.2.5.jar \
    && echo 'ed62e2fde3a4e832f409b2164fe5e16aa19b851b9cbfc3474352c16094a56994  /work/lib/ph-annotations-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jspecify/jspecify/1.0.0/jspecify-1.0.0.jar -o /work/lib/jspecify-1.0.0.jar \
    && echo '1fad6e6be7557781e4d33729d49ae1cdc8fdda6fe477bb0cc68ce351eafdfbab  /work/lib/jspecify-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-statistics/12.2.5/ph-statistics-12.2.5.jar -o /work/lib/ph-statistics-12.2.5.jar \
    && echo 'f46fb82ea85174b8227ca12bcdf34ebe909e4c04d9743e214cecc9053df38810  /work/lib/ph-statistics-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-io/12.2.5/ph-io-12.2.5.jar -o /work/lib/ph-io-12.2.5.jar \
    && echo 'a521cdca60dd54c0c350dc5783f92ccda0c34ef58fd7568e5f69d01699766ba9  /work/lib/ph-io-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-mime/12.2.5/ph-mime-12.2.5.jar -o /work/lib/ph-mime-12.2.5.jar \
    && echo '59bb887768f6b43c68cf3e8c54100017c20eab5e7841f3194a89ec6e8c8b8795  /work/lib/ph-mime-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/helger/commons/ph-text/12.2.5/ph-text-12.2.5.jar -o /work/lib/ph-text-12.2.5.jar \
    && echo '657bdb5b959f15a65e1a0d3b43f3b8335134d8ec264ca21e68fe0ba85d9e9cad  /work/lib/ph-text-12.2.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/groovy/groovy/5.1.1/groovy-5.1.1.jar -o /work/lib/groovy-5.1.1.jar \
    && echo '550a072831e036aa3f6508520df1c1cb91633efa0d7d9e800a07a74227059a47  /work/lib/groovy-5.1.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/furutuki/transcoder-core/0.1.1/transcoder-core-0.1.1.jar -o /work/lib/transcoder-core-0.1.1.jar \
    && echo '64305fdedee3e178ec458af1b3ff50e6ec043b0a85d0eb71f40ab435fd94e150  /work/lib/transcoder-core-0.1.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-batik/3.15.2/imageio-batik-3.15.2.jar -o /work/lib/imageio-batik-3.15.2.jar \
    && echo '664503f96fe3aab70962c19de78a0265a26db29c1a11bec7373238ee64427610  /work/lib/imageio-batik-3.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-core/3.15.2/imageio-core-3.15.2.jar -o /work/lib/imageio-core-3.15.2.jar \
    && echo '7f753d7305e11e715d837957f56f4b2c2cd9ad6973d4fb80aec6ce220c196912  /work/lib/imageio-core-3.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-lang/3.15.2/common-lang-3.15.2.jar -o /work/lib/common-lang-3.15.2.jar \
    && echo '06bc0995d2f1fe89ecbf2834701095833fb506c79be6f9cf27ee5b09528f578d  /work/lib/common-lang-3.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-io/3.15.2/common-io-3.15.2.jar -o /work/lib/common-io-3.15.2.jar \
    && echo '9e23601e28682f5c0947b4c34f373889315263e653975c9265e22e492d4d5e67  /work/lib/common-io-3.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-image/3.15.2/common-image-3.15.2.jar -o /work/lib/common-image-3.15.2.jar \
    && echo '2f293a4d247ead6588b0f70336412494723e77df2d814549fbdb08fd7619eec3  /work/lib/common-image-3.15.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/bweng20/jSVGIcon/1.6/jSVGIcon-1.6.jar -o /work/lib/jSVGIcon-1.6.jar \
    && echo 'ffb1cef57bee15e21303c695419873a9dd93ae3f5314dc3838e0258843d9bb79  /work/lib/jSVGIcon-1.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/weisj/jsvg/2.0.0/jsvg-2.0.0.jar -o /work/lib/jsvg-2.0.0.jar \
    && echo '81fc9ada579fc3f4924ec35f904c043de13ee8fba280322e638c7092006f1b52  /work/lib/jsvg-2.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/blackears/svg-salamander/1.1.5.5/svg-salamander-1.1.5.5.jar -o /work/lib/svg-salamander-1.1.5.5.jar \
    && echo 'e29d64853993ecf3d65d07ce458c12f0b908917cceaf485e3a3560473f322f17  /work/lib/svg-salamander-1.1.5.5.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/furutuki/transcoder-core/0.1.1/transcoder-core-0.1.1-sources.jar -o /work/parser-sources.jar \
    && echo 'bb349b5335c0be4ce330177284f0d2a8844568bdd8ff44beb21c254d24aa0a2c  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SvgAdapter.java GenericHarness.java /work/src/
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
