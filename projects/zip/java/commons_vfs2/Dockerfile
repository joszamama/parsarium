FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-compress/1.28.0/commons-compress-1.28.0.jar -o /work/lib/commons-compress-1.28.0.jar \
    && echo 'e1522945218456f3649a39bc4afd70ce4bd466221519dba7d378f2141a4642ca  /work/lib/commons-compress-1.28.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.19.0/commons-codec-1.19.0.jar -o /work/lib/commons-codec-1.19.0.jar \
    && echo '5c3881e4f556855e9c532927ee0c9dfde94cc66760d5805c031a59887070af5f  /work/lib/commons-codec-1.19.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.20.0/commons-io-2.20.0.jar -o /work/lib/commons-io-2.20.0.jar \
    && echo 'df90bba0fe3cb586b7f164e78fe8f8f4da3f2dd5c27fa645f888100ccc25dd72  /work/lib/commons-io-2.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.18.0/commons-lang3-3.18.0.jar -o /work/lib/commons-lang3-3.18.0.jar \
    && echo '4eeeae8d20c078abb64b015ec158add383ac581571cddc45c68f0c9ae0230720  /work/lib/commons-lang3-3.18.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/lingala/zip4j/zip4j/2.11.6/zip4j-2.11.6.jar -o /work/lib/zip4j-2.11.6.jar \
    && echo '5f1eb1e9d67cfee200a695e4079751b49e73a226b154193e13f7c602efbe72fb  /work/lib/zip4j-2.11.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/zeroturnaround/zt-zip/1.18.2/zt-zip-1.18.2.jar -o /work/lib/zt-zip-1.18.2.jar \
    && echo '6330946d07c42b39aefad49f8318dee096a7fb5d0d57227e8feb59167bb17cff  /work/lib/zt-zip-1.18.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/2.0.18/slf4j-api-2.0.18.jar -o /work/lib/slf4j-api-2.0.18.jar \
    && echo '44508fd1576500688c790b190acdd16fec4f8c79a3e0b900afd70503cf055f55  /work/lib/slf4j-api-2.0.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/software/coley/lljzip/2.1.0/lljzip-2.1.0.jar -o /work/lib/lljzip-2.1.0.jar \
    && echo 'bf9ae7dc86cae891b5d04a5f696ab008a16511b89ddb9adf2b42413bff91b60e  /work/lib/lljzip-2.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar -o /work/lib/jsr305-3.0.2.jar \
    && echo '766ad2a0783f2687962c8ad74ceecc38a28b9f72a2d085ee438b7813e928d0c7  /work/lib/jsr305-3.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/ant/ant/1.10.18/ant-1.10.18.jar -o /work/lib/ant-1.10.18.jar \
    && echo 'a12d775f581ad87592b1b1c7ff6fa5bcf6bb784974b94c848b0695ae15765f46  /work/lib/ant-1.10.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/ant/ant-launcher/1.10.18/ant-launcher-1.10.18.jar -o /work/lib/ant-launcher-1.10.18.jar \
    && echo 'b96e61ec45a9cbb2cf8d009c47ca544b451f419df105195a919205af7af47aa2  /work/lib/ant-launcher-1.10.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-vfs2/2.10.0/commons-vfs2-2.10.0.jar -o /work/lib/commons-vfs2-2.10.0.jar \
    && echo 'adf9dfb77a44f7b6e2dba3779cfa7142ab8a1f618eb7a9741083822e8d14be13  /work/lib/commons-vfs2-2.10.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.3.4/commons-logging-1.3.4.jar -o /work/lib/commons-logging-1.3.4.jar \
    && echo 'bc2dfe32f1ef06509e6a065144c1adf7b420eabf11a87f30bd127f8faa332016  /work/lib/commons-logging-1.3.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ru/oleg-cherednik/zip4jvm/zip4jvm/1.13/zip4jvm-1.13.jar -o /work/lib/zip4jvm-1.13.jar \
    && echo 'ffa74948925f8a026896963531c4745959fa6814b82ff842f9a56ed7c61f93c2  /work/lib/zip4jvm-1.13.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/luben/zstd-jni/1.5.7-3/zstd-jni-1.5.7-3.jar -o /work/lib/zstd-jni-1.5.7-3.jar \
    && echo 'a38a4a97f1b43b878c91e0dd7f1e3d17f0e70beec71d95bacaf56a2f207624a3  /work/lib/zstd-jni-1.5.7-3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/tukaani/xz/1.10/xz-1.10.jar -o /work/lib/xz-1.10.jar \
    && echo '95c63c1a55b22dd6453890a419cc1a640f790bbf7d8ae82db1e30aefefb08888  /work/lib/xz-1.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/quarkus/quarkus-fs-util/1.4.2/quarkus-fs-util-1.4.2.jar -o /work/lib/quarkus-fs-util-1.4.2.jar \
    && echo 'a6034133b21de4e3aee4bc9e250f8416abfbdc0c86e6e0737f766415c3866169  /work/lib/quarkus-fs-util-1.4.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/plexus/plexus-archiver/4.15.0/plexus-archiver-4.15.0.jar -o /work/lib/plexus-archiver-4.15.0.jar \
    && echo '897010dfebcc9339f36abef8b3b2a6879f49a8b93d83e3881b9fb6b0b382cd5b  /work/lib/plexus-archiver-4.15.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/javax/inject/javax.inject/1/javax.inject-1.jar -o /work/lib/javax.inject-1.jar \
    && echo '91c77044a50c481636c32d916fd89c9118a72195390452c81065080f957de7ff  /work/lib/javax.inject-1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/plexus/plexus-utils/3.6.2/plexus-utils-3.6.2.jar -o /work/lib/plexus-utils-3.6.2.jar \
    && echo '7c2cdf8b4a02a2ee3f0514b8d74ad5eb6e2365eeb073a5cabd6f2d61d8f871df  /work/lib/plexus-utils-3.6.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/plexus/plexus-io/3.8.0/plexus-io-3.8.0.jar -o /work/lib/plexus-io-3.8.0.jar \
    && echo 'e388633a2cf05d2569c0a3887351f3f34e777dde5c5482bfb9749c2ecb9f483b  /work/lib/plexus-io-3.8.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/rauschig/jarchivelib/1.2.0/jarchivelib-1.2.0.jar -o /work/lib/jarchivelib-1.2.0.jar \
    && echo '524142e431fc739120d961457c29ac1f9d384ab03265aaef2d6aa39677c9ad93  /work/lib/jarchivelib-1.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/hominux/compress4j/5.1.0/compress4j-5.1.0.jar -o /work/lib/compress4j-5.1.0.jar \
    && echo '571d0adfc7beef7c2e58c371dc89ed1ff91a0bdff4fe4c83fd1df16d7c68be34  /work/lib/compress4j-5.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jspecify/jspecify/1.0.1/jspecify-1.0.1.jar -o /work/lib/jspecify-1.0.1.jar \
    && echo '070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66  /work/lib/jspecify-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/realburst/arcana/1.1.0/arcana-1.1.0.jar -o /work/lib/arcana-1.1.0.jar \
    && echo '316d3da8dd032fe62bd3b6b099c45af90c01186c90ce433f07375d8413566706  /work/lib/arcana-1.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-pkg-module/4.2.0/tika-parser-pkg-module-4.2.0.jar -o /work/lib/tika-parser-pkg-module-4.2.0.jar \
    && echo '65d5ee06105e718ed34c404914f0af0eef0bde65d64f16a2e65bde8d1f7ae6bb  /work/lib/tika-parser-pkg-module-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/brotli/dec/0.1.2/dec-0.1.2.jar -o /work/lib/dec-0.1.2.jar \
    && echo '615c0c3efef990d77831104475fba6a1f7971388691d4bad1471ad84101f6d52  /work/lib/dec-0.1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-zip-commons/4.2.0/tika-parser-zip-commons-4.2.0.jar -o /work/lib/tika-parser-zip-commons-4.2.0.jar \
    && echo '9358ee17df2aeed44d5df9863e1e7ca491d8bf0dcb7ed350d673f0e024e5c683  /work/lib/tika-parser-zip-commons-4.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/junrar/junrar/8.1.2/junrar-8.1.2.jar -o /work/lib/junrar-8.1.2.jar \
    && echo '6f8204a7fa257af3fb127d0d71176bc5f55d9a572fc576d02d67bf79def19b15  /work/lib/junrar-8.1.2.jar' | sha256sum --check \
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
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-driver-zip/7.7.10/truezip-driver-zip-7.7.10.jar -o /work/lib/truezip-driver-zip-7.7.10.jar \
    && echo 'a5467acf334972258154d52706f4f135e9b975f1f2161c8e895f48b78b2b1890  /work/lib/truezip-driver-zip-7.7.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-swing/7.7.10/truezip-swing-7.7.10.jar -o /work/lib/truezip-swing-7.7.10.jar \
    && echo '1c78511ac31da511ac9665f27c7ef08f34c2f36e9ec766ed193e8d011b082f2c  /work/lib/truezip-swing-7.7.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/code/findbugs/annotations/3.0.0/annotations-3.0.0.jar -o /work/lib/annotations-3.0.0.jar \
    && echo '9dc756a03800f000781c5e2feddb67e5d4174b2e3f7f78c2021bf4e95c64adf1  /work/lib/annotations-3.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk15on/1.52/bcprov-jdk15on-1.52.jar -o /work/lib/bcprov-jdk15on-1.52.jar \
    && echo '0dc4d181e4d347893c2ddbd2e6cd5d7287fc651c03648fa64b2341c7366b1773  /work/lib/bcprov-jdk15on-1.52.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-kernel/7.7.10/truezip-kernel-7.7.10.jar -o /work/lib/truezip-kernel-7.7.10.jar \
    && echo '23a9fdfcc61b4db75cf4c91a9e99b6940e1a8ac600e718e4d143c9c7a1139777  /work/lib/truezip-kernel-7.7.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-driver-file/7.7.10/truezip-driver-file-7.7.10.jar -o /work/lib/truezip-driver-file-7.7.10.jar \
    && echo 'd9eff4b24fccd3cc9a95786684f753b595aa062f23aa1366cc860c6355b26cfc  /work/lib/truezip-driver-file-7.7.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-file/7.7.10/truezip-file-7.7.10.jar -o /work/lib/truezip-file-7.7.10.jar \
    && echo 'ae670babc8eb4a890c5a8436a6ddb0680fc6d9c5f10e585ea0ab25636cdfa0de  /work/lib/truezip-file-7.7.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/deepakdaneva/commons/commons-archive/1.1.0/commons-archive-1.1.0.jar -o /work/lib/commons-archive-1.1.0.jar \
    && echo '00edc9f7d2eb80366421d9b26cbdb680b033d4fbbaa05541132acd109e6faf49  /work/lib/commons-archive-1.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/codehaus/mojo/truezip-utils/1.2/truezip-utils-1.2.jar -o /work/lib/truezip-utils-1.2.jar \
    && echo '756c0b679aabb3bbeb6375b9bb365bdc6f46f33aae3408b06793ffae4e120721  /work/lib/truezip-utils-1.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/de/schlichtherle/truezip/truezip-driver-tar/7.7.5/truezip-driver-tar-7.7.5.jar -o /work/lib/truezip-driver-tar-7.7.5.jar \
    && echo 'e64018ce5151b3aae61fe8b13738deec06c5c5dd2b6a5a762d2a403aa5d31b49  /work/lib/truezip-driver-tar-7.7.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/maven/shared/file-management/1.2.1/file-management-1.2.1.jar -o /work/lib/file-management-1.2.1.jar \
    && echo '009478892149c0141645276d2c74094e7db595a48765b74834565b1dd25b454e  /work/lib/file-management-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-lang/commons-lang/2.4/commons-lang-2.4.jar -o /work/lib/commons-lang-2.4.jar \
    && echo '2c73b940c91250bc98346926270f13a6a10bb6e29d2c9316a70d134e382c873e  /work/lib/commons-lang-2.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/j256/simplezip/simplezip/2.2/simplezip-2.2.jar -o /work/lib/simplezip-2.2.jar \
    && echo 'ef0ba61b9318fecb7629a0bd2aa270cddbdcb400c737a3a8cf4733f9456d42d7  /work/lib/simplezip-2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/github/bitstorm/tinyzip-core/1.0.0/tinyzip-core-1.0.0.jar -o /work/lib/tinyzip-core-1.0.0.jar \
    && echo '7dd20146944eba589ca0902bf327c458486cfc9dd86b21d4eb8eb1effc70e4d1  /work/lib/tinyzip-core-1.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sf/sevenzipjbinding/sevenzipjbinding/23.01-2.2/sevenzipjbinding-23.01-2.2.jar -o /work/lib/sevenzipjbinding-23.01-2.2.jar \
    && echo '2cb5368ef44372df91b6def8722f6e68357453160872a918f931762954a78d60  /work/lib/sevenzipjbinding-23.01-2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/sf/sevenzipjbinding/sevenzipjbinding-all-platforms/23.01-2.2/sevenzipjbinding-all-platforms-23.01-2.2.jar -o /work/lib/sevenzipjbinding-all-platforms-23.01-2.2.jar \
    && echo '2f60e6075a7bb2290970774fabcbd61cbeca9e9b0cdbbe36999d5438c69f536a  /work/lib/sevenzipjbinding-all-platforms-23.01-2.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-access/0.14.0/truevfs-access-0.14.0.jar -o /work/lib/truevfs-access-0.14.0.jar \
    && echo '2187354eeb8b766aa91210b9eece6f0e24102d4658e1721ad59fea3748d720e5  /work/lib/truevfs-access-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-driver-file/0.14.0/truevfs-driver-file-0.14.0.jar -o /work/lib/truevfs-driver-file-0.14.0.jar \
    && echo '015019c98a676b10e90b5947489a2e05e6c692babcf1330256510d0cee43e08b  /work/lib/truevfs-driver-file-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-kernel-spec/0.14.0/truevfs-kernel-spec-0.14.0.jar -o /work/lib/truevfs-kernel-spec-0.14.0.jar \
    && echo '890590596fda3796601c517e7b27610d88bb3d6111a153c872c0eba34fc41e28  /work/lib/truevfs-kernel-spec-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/global/namespace/service-wight/service-wight-core/0.6.0/service-wight-core-0.6.0.jar -o /work/lib/service-wight-core-0.6.0.jar \
    && echo '7d49c587f165e796470356eb06cc4390539a8c0e528d6ea24e0c843323db1a57  /work/lib/service-wight-core-0.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-cio/2.5.0/truecommons-cio-2.5.0.jar -o /work/lib/truecommons-cio-2.5.0.jar \
    && echo '61a0db290c036fbf44743113a714b50e5112ff3ffb9f7a817aa0eaed9ef978bb  /work/lib/truecommons-cio-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-io/2.5.0/truecommons-io-2.5.0.jar -o /work/lib/truecommons-io-2.5.0.jar \
    && echo 'b6ef4065d2567076d2c234697929d5936fe7bc86149f78fb93be156e05d7a312  /work/lib/truecommons-io-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-kernel-impl/0.14.0/truevfs-kernel-impl-0.14.0.jar -o /work/lib/truevfs-kernel-impl-0.14.0.jar \
    && echo '4bcb55bf8d74c0a3245c81f3f85f9bd3895572a53daf114f4e45f4e71e764166  /work/lib/truevfs-kernel-impl-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-logging/2.5.0/truecommons-logging-2.5.0.jar -o /work/lib/truecommons-logging-2.5.0.jar \
    && echo 'a791a0c23a724aa920b9a4dee3801569948ac29c4bbc7b5abb1f3fc4534db605  /work/lib/truecommons-logging-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-services/2.5.0/truecommons-services-2.5.0.jar -o /work/lib/truecommons-services-2.5.0.jar \
    && echo 'edec057e71c53620460d4c49448e4d32d988da6042419e1372aa6bce463c3ee7  /work/lib/truecommons-services-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-driver-zip/0.14.0/truevfs-driver-zip-0.14.0.jar -o /work/lib/truevfs-driver-zip-0.14.0.jar \
    && echo 'b60bc5e489aa775b18f320132bae86c1eca00ed764aee388870c3485fdd32c28  /work/lib/truevfs-driver-zip-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-comp-ibm437/0.14.0/truevfs-comp-ibm437-0.14.0.jar -o /work/lib/truevfs-comp-ibm437-0.14.0.jar \
    && echo '9e1f29d4e119422d29b85fdb6c703b4dabd89dfa7c196ba5207e5d8e46dab4aa  /work/lib/truevfs-comp-ibm437-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/global/namespace/service-wight/service-wight-annotation/0.6.0/service-wight-annotation-0.6.0.jar -o /work/lib/service-wight-annotation-0.6.0.jar \
    && echo 'a257eafc102b84c8732b19040afdf067c1611e2298c42104dc3f557bd115f9ba  /work/lib/service-wight-annotation-0.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-comp-zipdriver/0.14.0/truevfs-comp-zipdriver-0.14.0.jar -o /work/lib/truevfs-comp-zipdriver-0.14.0.jar \
    && echo '23a63bc4ff1b91c7ff287a18f6bd18fa758998a1ee734d7c4180fab8ec5fb662  /work/lib/truevfs-comp-zipdriver-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truevfs/truevfs-comp-zip/0.14.0/truevfs-comp-zip-0.14.0.jar -o /work/lib/truevfs-comp-zip-0.14.0.jar \
    && echo '92a3d0136a7e2367210e768975e5d92d07d4648e6d411c92ae5e1af66b7372c2  /work/lib/truevfs-comp-zip-0.14.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-key-default/2.5.0/truecommons-key-default-2.5.0.jar -o /work/lib/truecommons-key-default-2.5.0.jar \
    && echo '90ee3487865b0ca38a529749a2b7fbffabf3d223a466157ec04e9dff72accc10  /work/lib/truecommons-key-default-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-key-spec/2.5.0/truecommons-key-spec-2.5.0.jar -o /work/lib/truecommons-key-spec-2.5.0.jar \
    && echo 'a7103fd23c95a80dc6c82be5a407a4e2c587fb74a087ff3808c0ccc20b4043f7  /work/lib/truecommons-key-spec-2.5.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/net/java/truecommons/truecommons-shed/2.5.0/truecommons-shed-2.5.0.jar -o /work/lib/truecommons-shed-2.5.0.jar \
    && echo '9b70bb63b79faa0e4c4b1aa820c610c1aa1c9fc9d4653edbe76a328f0d3c1a75  /work/lib/truecommons-shed-2.5.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-vfs2/2.10.0/commons-vfs2-2.10.0-sources.jar -o /work/parser-sources.jar \
    && echo '8a87831e1bebbb78ed537770ee1aa623db656c1509f92284cbcaa4266525ab7f  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY ZipAdapter.java GenericHarness.java /work/src/
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
