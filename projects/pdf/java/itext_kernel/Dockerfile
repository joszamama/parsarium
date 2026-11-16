FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox/3.0.8/pdfbox-3.0.8.jar -o /work/lib/pdfbox-3.0.8.jar \
    && echo '97647cfbde61ebcfc06b4cf8c9b0ffcaaee073396eceb4a7f6836a9b9128903c  /work/lib/pdfbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox-io/3.0.8/pdfbox-io-3.0.8.jar -o /work/lib/pdfbox-io-3.0.8.jar \
    && echo '36a0e04001010b4c764857817412b96339930b19755e728959805cc0352061b2  /work/lib/pdfbox-io-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/fontbox/3.0.8/fontbox-3.0.8.jar -o /work/lib/fontbox-3.0.8.jar \
    && echo 'a1915c24e3edbe0ecec93896dfbf6d41427810b663ade97bd4e8bae86ec3fdab  /work/lib/fontbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.4.0/commons-logging-1.4.0.jar -o /work/lib/commons-logging-1.4.0.jar \
    && echo 'd175dbd751dd782a63bde28c7a039520e971f25e84b79c19b8435edc3603e0dc  /work/lib/commons-logging-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/itextpdf/5.5.13/itextpdf-5.5.13.jar -o /work/lib/itextpdf-5.5.13.jar \
    && echo '368500a5f57fd0b04e565e78cfe469e61c362e86445667a29c9645dd2ce10b3d  /work/lib/itextpdf-5.5.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/librepdf/openpdf/3.0.5/openpdf-3.0.5.jar -o /work/lib/openpdf-3.0.5.jar \
    && echo '2a70c6024bb10b6192b4b91d8bb581de24b776a799a30ef5b87748e54aca2144  /work/lib/openpdf-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/brotli4j/1.23.0/brotli4j-1.23.0.jar -o /work/lib/brotli4j-1.23.0.jar \
    && echo '5fcf13ad78d07319cc507465dcf61cbc3efee9f45c9ae1c42a9902414696bc0b  /work/lib/brotli4j-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/service/1.23.0/service-1.23.0.jar -o /work/lib/service-1.23.0.jar \
    && echo '7f298d44dbb7688419f0179ee1dfa0e4436633272b05d38a5faf3a2b8d08697b  /work/lib/service-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/aayushatharva/brotli4j/native-osx-aarch64/1.23.0/native-osx-aarch64-1.23.0.jar -o /work/lib/native-osx-aarch64-1.23.0.jar \
    && echo 'be3bc53688dbaff26d9d554301837de2bfa9ec09090b64d1ebf1fb6b23c28e61  /work/lib/native-osx-aarch64-1.23.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/kernel/9.8.0/kernel-9.8.0.jar -o /work/lib/kernel-9.8.0.jar \
    && echo 'f0e4ae6ba1fc52e9332aa827206e4848ddc0fb69fb138988d9760462d75a0877  /work/lib/kernel-9.8.0.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/bouncy-castle-connector/9.8.0/bouncy-castle-connector-9.8.0.jar -o /work/lib/bouncy-castle-connector-9.8.0.jar \
    && echo '04b0eaf8de7244c06f284c67c765e5f91c6edb34098c853affcc3a30b9165163  /work/lib/bouncy-castle-connector-9.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.16/slf4j-api-2.0.16.jar -o /work/lib/slf4j-api-2.0.16.jar \
    && echo 'a12578dde1ba00bd9b816d388a0b879928d00bab3c83c240f7013bf4196c579a  /work/lib/slf4j-api-2.0.16.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-pdf-module/4.2.0/tika-parser-pdf-module-4.2.0.jar -o /work/lib/tika-parser-pdf-module-4.2.0.jar \
    && echo 'f2f14ff56531bee9101b9bfaadcce1d3176373abdf32208b56020f1c283e0aab  /work/lib/tika-parser-pdf-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-xmp-commons/4.2.0/tika-parser-xmp-commons-4.2.0.jar -o /work/lib/tika-parser-xmp-commons-4.2.0.jar \
    && echo '89860eadfb83934d1d6c7d1990e12568fc3d41028f4bf1c1310fe84b8da0413c  /work/lib/tika-parser-xmp-commons-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox-tools/3.0.8/pdfbox-tools-3.0.8.jar -o /work/lib/pdfbox-tools-3.0.8.jar \
    && echo '73091ece9b8a15bc7f946c224aaec2f7b3104b4c24f1978122ddd452ddc0a578  /work/lib/pdfbox-tools-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/info/picocli/picocli/4.7.7/picocli-4.7.7.jar -o /work/lib/picocli-4.7.7.jar \
    && echo 'f86e30fffd10d2b13b8caa8d4b237a7ee61f2ffccf5b1941de718b765d235bf8  /work/lib/picocli-4.7.7.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcjmail-jdk18on/1.86/bcjmail-jdk18on-1.86.jar -o /work/lib/bcjmail-jdk18on-1.86.jar \
    && echo 'a6c26f418de462f7f3e575de7561fa5af1995c220f236515963b56f31c347acb  /work/lib/bcjmail-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcpkix-jdk18on/1.86/bcpkix-jdk18on-1.86.jar -o /work/lib/bcpkix-jdk18on-1.86.jar \
    && echo '8d8b41a4b149bdae8d331f059a578870954d1e3ff29f8269a9eb3ee19a7e4ef7  /work/lib/bcpkix-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcutil-jdk18on/1.86/bcutil-jdk18on-1.86.jar -o /work/lib/bcutil-jdk18on-1.86.jar \
    && echo '1c268e15f785aafb1e4670d8d6e5f856f69475e96c162dadcd1ff9b350e9139f  /work/lib/bcutil-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk18on/1.86/bcprov-jdk18on-1.86.jar -o /work/lib/bcprov-jdk18on-1.86.jar \
    && echo '2af190b300cbb0b35e248ccf5f4a06b6072030aeb3da7a98ec73abe5b4cb371f  /work/lib/bcprov-jdk18on-1.86.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/pdfjet/pdfjet/9.1.7/pdfjet-9.1.7.jar -o /work/lib/pdfjet-9.1.7.jar \
    && echo 'ca817dddef53a784a03c6dd6cadf96e20b1d169155957a3303414a41375b7f49  /work/lib/pdfjet-9.1.7.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/icepdf/os/icepdf-core/6.2.2/icepdf-core-6.2.2.jar -o /work/lib/icepdf-core-6.2.2.jar \
    && echo 'c21cf9be3045ebfeed757643c9417a3bc65235c278652c88cbcaea0bdebef54f  /work/lib/icepdf-core-6.2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk15on/1.54/bcprov-jdk15on-1.54.jar -o /work/lib/bcprov-jdk15on-1.54.jar \
    && echo 'd0ae14598f9c528d2ab7bb8ed00e785a5440f692712cd362d69328aba25efb57  /work/lib/bcprov-jdk15on-1.54.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-ext-jdk15on/1.54/bcprov-ext-jdk15on-1.54.jar -o /work/lib/bcprov-ext-jdk15on-1.54.jar \
    && echo '538e61405561a29321609520bd13948c7724bbe3f84f7d6e61e81102c5837529  /work/lib/bcprov-ext-jdk15on-1.54.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcpkix-jdk15on/1.54/bcpkix-jdk15on-1.54.jar -o /work/lib/bcpkix-jdk15on-1.54.jar \
    && echo 'd618dcfbf0337b91015b21d4b398175ae96382a82c7e1d6e8c657fcd236463c7  /work/lib/bcpkix-jdk15on-1.54.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/sun/media/jai_imageio/1.1/jai_imageio-1.1.pom -o /work/lib/jai_imageio-1.1.pom \
    && echo 'a6505da0f7a01e265e5926c56e3ab6bb951911c8f610312967a632652ea8040c  /work/lib/jai_imageio-1.1.pom' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/preflight/3.0.8/preflight-3.0.8.jar -o /work/lib/preflight-3.0.8.jar \
    && echo '375a5d2c93cac48934354f146df91074eaec9c01816346e5e956543541e87e69  /work/lib/preflight-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/xmpbox/3.0.8/xmpbox-3.0.8.jar -o /work/lib/xmpbox-3.0.8.jar \
    && echo 'f044d2e316e57714a0adf272ad8abf4a863b8978fd17dc5b86dcfa8135469b10  /work/lib/xmpbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/librepdf/openpdf-renderer/3.0.5/openpdf-renderer-3.0.5.jar -o /work/lib/openpdf-renderer-3.0.5.jar \
    && echo '7b2c3976cd2db7f11c3047902fa35454f65e3cecc18b436a7635fe503da74c31  /work/lib/openpdf-renderer-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/verapdf/parser/1.30.4/parser-1.30.4.jar -o /work/lib/parser-1.30.4.jar \
    && echo 'f8a5c8d5d6ba13ccd70fb24bd996b5e22431c20679ddd89bf3a67848a3e3aef9  /work/lib/parser-1.30.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/dlsc/pdfviewfx/pdfviewfx/3.6.1/pdfviewfx-3.6.1.jar -o /work/lib/pdfviewfx-3.6.1.jar \
    && echo '66dd6cb28fffb725bcb9e44158ceda4d7319de13672f5948a1429b64b31d946b  /work/lib/pdfviewfx-3.6.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-controls/23.0.2/javafx-controls-23.0.2.jar -o /work/lib/javafx-controls-23.0.2.jar \
    && echo 'c83957342e7d3bc858ace6219a091e324fbde29f48f47a785ba313685c17f0e4  /work/lib/javafx-controls-23.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-controls/23.0.2/javafx-controls-23.0.2-mac-aarch64.jar -o /work/lib/javafx-controls-23.0.2-mac-aarch64.jar \
    && echo '39d923ab76f456784f189ff022a5437994726c79f40680540060a16cb259631f  /work/lib/javafx-controls-23.0.2-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-graphics/23.0.2/javafx-graphics-23.0.2.jar -o /work/lib/javafx-graphics-23.0.2.jar \
    && echo '3fb45f728e30a64202c08e72da2e2718659f8712b42eee601e658740482a897e  /work/lib/javafx-graphics-23.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-graphics/23.0.2/javafx-graphics-23.0.2-mac-aarch64.jar -o /work/lib/javafx-graphics-23.0.2-mac-aarch64.jar \
    && echo '774f9d4980980730573e5b56f335203507522b7961953d8ed9a7a32b064c201e  /work/lib/javafx-graphics-23.0.2-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-base/23.0.2/javafx-base-23.0.2.jar -o /work/lib/javafx-base-23.0.2.jar \
    && echo '9a12c46e92d617785fc296251754ae4b406494110d44cbc2a0a018cabe189c5c  /work/lib/javafx-base-23.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-base/23.0.2/javafx-base-23.0.2-mac-aarch64.jar -o /work/lib/javafx-base-23.0.2-mac-aarch64.jar \
    && echo '1e0b22c5a79239df71f7658379d896acc6f37411ce78d1235d6c3839defdfbeb  /work/lib/javafx-base-23.0.2-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-swing/23.0.2/javafx-swing-23.0.2.jar -o /work/lib/javafx-swing-23.0.2.jar \
    && echo 'dd89cf3dcbd633338311981ce117f9b2bdf617f8e5210bebad2a4c6c7ffc7313  /work/lib/javafx-swing-23.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/openjfx/javafx-swing/23.0.2/javafx-swing-23.0.2-mac-aarch64.jar -o /work/lib/javafx-swing-23.0.2-mac-aarch64.jar \
    && echo '660c433d078bcf86b3f08110558c6e727529ef666e82f87802673a2ef9c5aee1  /work/lib/javafx-swing-23.0.2-mac-aarch64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/controlsfx/controlsfx/11.2.4/controlsfx-11.2.4.jar -o /work/lib/controlsfx-11.2.4.jar \
    && echo '13aa76f92e3cb3fe32c8d8c9d96e58e2d55b28d951aebf0181efcbd6a7b2d21e  /work/lib/controlsfx-11.2.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/kordamp/ikonli/ikonli-core/12.4.0/ikonli-core-12.4.0.jar -o /work/lib/ikonli-core-12.4.0.jar \
    && echo 'ff938c94640d498be34d955f6353c9caf5aa66039842a735018820acbdc61fb4  /work/lib/ikonli-core-12.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/kordamp/ikonli/ikonli-materialdesign-pack/12.4.0/ikonli-materialdesign-pack-12.4.0.jar -o /work/lib/ikonli-materialdesign-pack-12.4.0.jar \
    && echo 'a6000ad0c421d33ebab34905716ed8100aa9694ec04fec77f5381c9d1313f024  /work/lib/ikonli-materialdesign-pack-12.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/kordamp/ikonli/ikonli-javafx/12.4.0/ikonli-javafx-12.4.0.jar -o /work/lib/ikonli-javafx-12.4.0.jar \
    && echo '0b606d7f7de5ee905046fbc301e3c127e46bcd8a58418180779e645123219e3c  /work/lib/ikonli-javafx-12.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.20.0/commons-lang3-3.20.0.jar -o /work/lib/commons-lang3-3.20.0.jar \
    && echo '69e5c9fa35da7a51a5fd2099dfe56a2d8d32cf233e2f6d770e796146440263f4  /work/lib/commons-lang3-3.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/sejda/sambox/4.0.0.M8/sambox-4.0.0.M8.jar -o /work/lib/sambox-4.0.0.M8.jar \
    && echo 'bc2133a5403065e30f0aa0e6322b55e0790849acbbb9204d55c545eb1de76aae  /work/lib/sambox-4.0.0.M8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/jcl-over-slf4j/2.0.19/jcl-over-slf4j-2.0.19.jar -o /work/lib/jcl-over-slf4j-2.0.19.jar \
    && echo 'efc3848f79638d9fa74ccbae3fd18c8735dcc0127b393ae53dce638827f8a2f3  /work/lib/jcl-over-slf4j-2.0.19.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/sejda/sejda-io/5.0.0.M1/sejda-io-5.0.0.M1.jar -o /work/lib/sejda-io-5.0.0.M1.jar \
    && echo 'a29fefeb9d8bfdc7d8b4a5c701d500e92fcd45c7aa59702780e77ecc63738074  /work/lib/sejda-io-5.0.0.M1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/sejda/sejda-commons/3.0.1/sejda-commons-3.0.1.jar -o /work/lib/sejda-commons-3.0.1.jar \
    && echo 'ea5c9b189cd162d40c0eb4d49fdbb1a3dbca8f193e433048868009e9bc46a4f7  /work/lib/sejda-commons-3.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/swinglabs/pdf-renderer/1.0.5/pdf-renderer-1.0.5.jar -o /work/lib/pdf-renderer-1.0.5.jar \
    && echo '100952e9852852642635c6c6993f7d5ce390b3a667dfdd52485c5ef25dd883a7  /work/lib/pdf-renderer-1.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/scireum/jpod/2.0/jpod-2.0.jar -o /work/lib/jpod-2.0.jar \
    && echo '80ace98cdfbba949e46a2ee36e08230cca0310b534e7ec026e9c8c4fab29ee4e  /work/lib/jpod-2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/intarsys/opensource/iscwt/5.5/iscwt-5.5.jar -o /work/lib/iscwt-5.5.jar \
    && echo '084e33f52132a61cb980ceb9e8f8122f733121c169dd320df7607d9d65f09900  /work/lib/iscwt-5.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/intarsys/opensource/isfreetype/5.5/isfreetype-5.5.jar -o /work/lib/isfreetype-5.5.jar \
    && echo '01e2651518fd87c5c19f563811d6fa7825b7b742153b41780794427adaab84b2  /work/lib/isfreetype-5.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/intarsys/opensource/isnativec/5.5/isnativec-5.5.jar -o /work/lib/isnativec-5.5.jar \
    && echo '5f5d98dabf05f2f1ba2d6141491cea82f10194276c0f709893eccee92bb65f6d  /work/lib/isnativec-5.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/intarsys/opensource/isrt/4.10/isrt-4.10.jar -o /work/lib/isrt-4.10.jar \
    && echo 'a56a741cbb4d37de4d1ca1ba8be242b064843abee2fec9281cc3ecca284a0233  /work/lib/isrt-4.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/intarsys/opensource/jbig2/5.5.1/jbig2-5.5.1.jar -o /work/lib/jbig2-5.5.1.jar \
    && echo '93e79e795182b4b6e12991046e489c2c0780e867d3e18e4e7ee20973316930d4  /work/lib/jbig2-5.5.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sourceforge/tess4j/tess4j/5.20.0/tess4j-5.20.0.jar -o /work/lib/tess4j-5.20.0.jar \
    && echo 'cb43baa95eb172a1f097db45991ef7518e76c8dacd4b467339b1e695abebfd4a  /work/lib/tess4j-5.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/dev/jna/jna/5.19.1/jna-5.19.1.jar -o /work/lib/jna-5.19.1.jar \
    && echo '4fb141dd8ef6b0585ffceea4bc49602fbc6312fa977e2c488794ea3e6aafecae  /work/lib/jna-5.19.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/jai-imageio/jai-imageio-core/1.4.0/jai-imageio-core-1.4.0.jar -o /work/lib/jai-imageio-core-1.4.0.jar \
    && echo '8ad3c68e9efffb10ac87ff8bc589adf64b04a729c5194c079efd0643607fd72a  /work/lib/jai-imageio-core-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/jbig2-imageio/3.0.5/jbig2-imageio-3.0.5.jar -o /work/lib/jbig2-imageio-3.0.5.jar \
    && echo 'd426cc8b6ac211dd5ffd120a86a65e55ae65d808c818207c1261bc1880b42653  /work/lib/jbig2-imageio-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sourceforge/lept4j/lept4j/1.24.0/lept4j-1.24.0.jar -o /work/lib/lept4j-1.24.0.jar \
    && echo '0e188426eb57662fe5c40ee5942b24403fcacbb7290dbe6fd215229c0ef91269  /work/lib/lept4j-1.24.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jboss/jboss-vfs/3.3.2.Final/jboss-vfs-3.3.2.Final.jar -o /work/lib/jboss-vfs-3.3.2.Final.jar \
    && echo '33a84eac3f1027551146247e3ef4057dc8840cfc8cd436cb2f925b6f5d2126e9  /work/lib/jboss-vfs-3.3.2.Final.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/itextpdf/kernel/9.8.0/kernel-9.8.0-sources.jar -o /work/parser-sources.jar \
    && echo '7f98c3632583a8bfbfdf3c44e9fc3bb13c7bf3d5f97fb47e950d060e80ce0888  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY PdfAdapter.java GenericHarness.java /work/src/
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
