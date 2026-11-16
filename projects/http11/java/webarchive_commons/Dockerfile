FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jodd/jodd-http/6.3.0/jodd-http-6.3.0.jar -o /work/lib/jodd-http-6.3.0.jar \
    && echo '4c800cdb752effa446219774b699175c223150d384c760c8ba28740a7ebbd6f3  /work/lib/jodd-http-6.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jodd/jodd-util/6.1.0/jodd-util-6.1.0.jar -o /work/lib/jodd-util-6.1.0.jar \
    && echo '8416b4d849aa07d58b86b1a7fb5447ef976af18fa4d68012862b8677f5ff67c2  /work/lib/jodd-util-6.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/athaydes/rawhttp/rawhttp-core/2.6.0/rawhttp-core-2.6.0.jar -o /work/lib/rawhttp-core-2.6.0.jar \
    && echo '76041cbc3f308aa7f61b61e93a08e87d1a130b5c0b3e1e735f5fd7143a3101d5  /work/lib/rawhttp-core-2.6.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/nanohttpd/nanohttpd/2.3.1/nanohttpd-2.3.1.jar -o /work/lib/nanohttpd-2.3.1.jar \
    && echo 'de864c47818157141a24c9acb36df0c47d7bf15b7ff48c90610f3eb4e5df0e58  /work/lib/nanohttpd-2.3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/netpreserve/jwarc/0.37.0/jwarc-0.37.0.jar -o /work/lib/jwarc-0.37.0.jar \
    && echo '070f87db9e2a98f3526b2a9637eddf3a2a66753bf1ad6483f6a23600824f4c9e  /work/lib/jwarc-0.37.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/netpreserve/commons/webarchive-commons/3.0.5/webarchive-commons-3.0.5.jar -o /work/lib/webarchive-commons-3.0.5.jar \
    && echo 'e67e1e997c9ac396c90f8acb8a2116bc8127fc6c946ff725c98a0d7b7b643a89  /work/lib/webarchive-commons-3.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/guava/33.7.1-jre/guava-33.7.1-jre.jar -o /work/lib/guava-33.7.1-jre.jar \
    && echo '796d8e28ac64e83a47c4c5935a8fecc4682650a04bbdead738ef0f5a3a0e6c46  /work/lib/guava-33.7.1-jre.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/failureaccess/1.0.3/failureaccess-1.0.3.jar -o /work/lib/failureaccess-1.0.3.jar \
    && echo 'cbfc3906b19b8f55dd7cfd6dfe0aa4532e834250d7f080bd8d211a3e246b59cb  /work/lib/failureaccess-1.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar -o /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar \
    && echo 'b372a037d4230aa57fbeffdef30fd6123f9c0c2db85d0aced00c91b974f33f99  /work/lib/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jspecify/jspecify/1.0.1/jspecify-1.0.1.jar -o /work/lib/jspecify-1.0.1.jar \
    && echo '070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66  /work/lib/jspecify-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/errorprone/error_prone_annotations/2.50.0/error_prone_annotations-2.50.0.jar -o /work/lib/error_prone_annotations-2.50.0.jar \
    && echo '4667724877f1d37a689202da191e23efa7657c62eef93ccdac406eccfe5cdd0a  /work/lib/error_prone_annotations-2.50.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/google/j2objc/j2objc-annotations/3.1/j2objc-annotations-3.1.jar -o /work/lib/j2objc-annotations-3.1.jar \
    && echo '84d3a150518485f8140ea99b8a985656749629f6433c92b80c75b36aba3b099b  /work/lib/j2objc-annotations-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/json/json/20260814/json-20260814.jar -o /work/lib/json-20260814.jar \
    && echo '7dd2de1533e766e2b6c07d8194da85145ad313a167a4760050f5c9b6839604fe  /work/lib/json-20260814.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/htmlparser/htmlparser/2.1/htmlparser-2.1.jar -o /work/lib/htmlparser-2.1.jar \
    && echo 'adfec88a2524334e1a728cfe7cbbf7ba3dc9131f4ea2127eeae3b70c2a59ce41  /work/lib/htmlparser-2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/htmlparser/htmllexer/2.1/htmllexer-2.1.jar -o /work/lib/htmllexer-2.1.jar \
    && echo '9fa936be55a07c18eac59ec53906e7219bbdd97625c5293e9847aa28cbfe9858  /work/lib/htmllexer-2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/googlecode/juniversalchardet/juniversalchardet/1.0.3/juniversalchardet-1.0.3.jar -o /work/lib/juniversalchardet-1.0.3.jar \
    && echo '757bfe906193b8b651e79dc26cd67d6b55d0770a2cdfb0381591504f779d4a76  /work/lib/juniversalchardet-1.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.22.1/commons-codec-1.22.1.jar -o /work/lib/commons-codec-1.22.1.jar \
    && echo '78a5d732fbd715e2d10bd7150d2f8030bae57267f8aacc5c88f642cb6c2e5d3f  /work/lib/commons-codec-1.22.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-cli/commons-cli/1.11.0/commons-cli-1.11.0.jar -o /work/lib/commons-cli-1.11.0.jar \
    && echo '8f7f8605d68e15bf32db61ec94eac6fdafc51b1bdbe1e0e0802b57d23f387792  /work/lib/commons-cli-1.11.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.20.0/commons-lang3-3.20.0.jar -o /work/lib/commons-lang3-3.20.0.jar \
    && echo '69e5c9fa35da7a51a5fd2099dfe56a2d8d32cf233e2f6d770e796146440263f4  /work/lib/commons-lang3-3.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-io/commons-io/2.22.0/commons-io-2.22.0.jar -o /work/lib/commons-io-2.22.0.jar \
    && echo '2b9a7b1f726fb86216dbd2c8321eabe0221dbd5b1be81c18e1cb53811b104758  /work/lib/commons-io-2.22.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/gnu/inet/libidn/1.44/libidn-1.44.jar -o /work/lib/libidn-1.44.jar \
    && echo '5252bfc470fc3f5f7c70a13c80e5e58accc83b9f3f4a6b02ee7c69ad049505b8  /work/lib/libidn-1.44.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jwat/jwat-common/1.2.1/jwat-common-1.2.1.jar -o /work/lib/jwat-common-1.2.1.jar \
    && echo 'e1f12634718c24d35f57a05e28c45590cb7e18b8a0a5398a793257d39f34e43c  /work/lib/jwat-common-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk15to18/1.65/bcprov-jdk15to18-1.65.jar -o /work/lib/bcprov-jdk15to18-1.65.jar \
    && echo '2dea4d470c07e29315a5b60a11a4fb377793f36e16fde15640db1f028f01b818  /work/lib/bcprov-jdk15to18-1.65.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/alibaba/csp/sentinel-transport-simple-http/1.8.10/sentinel-transport-simple-http-1.8.10.jar -o /work/lib/sentinel-transport-simple-http-1.8.10.jar \
    && echo '8d78c6248323a972b1a23c7237367f2d34313e9c231afa9cda86595e38ea1189  /work/lib/sentinel-transport-simple-http-1.8.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/alibaba/csp/sentinel-transport-common/1.8.10/sentinel-transport-common-1.8.10.jar -o /work/lib/sentinel-transport-common-1.8.10.jar \
    && echo '93f909cca709b5c632e8e731ecffb65c2f4e2857e9ad39e87ce264fe847564f5  /work/lib/sentinel-transport-common-1.8.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/alibaba/csp/sentinel-datasource-extension/1.8.10/sentinel-datasource-extension-1.8.10.jar -o /work/lib/sentinel-datasource-extension-1.8.10.jar \
    && echo '98e6bb35dfa2161916f4d365ed2db9ce07340373136c4f9c2b521fd1328c1112  /work/lib/sentinel-datasource-extension-1.8.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/alibaba/csp/sentinel-core/1.8.10/sentinel-core-1.8.10.jar -o /work/lib/sentinel-core-1.8.10.jar \
    && echo 'd446e0125d49b0668cfe067008c6518e0e2ca960859a85fa1079a1d1810f8900  /work/lib/sentinel-core-1.8.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/alibaba/fastjson/1.2.83_noneautotype/fastjson-1.2.83_noneautotype.jar -o /work/lib/fastjson-1.2.83_noneautotype.jar \
    && echo '10966bdcb594e156627b97559458433b096905358aa61f5f0ad9b3f1bba04166  /work/lib/fastjson-1.2.83_noneautotype.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/httpcomponents/httpcore-nio/4.4.16/httpcore-nio-4.4.16.jar -o /work/lib/httpcore-nio-4.4.16.jar \
    && echo '4018736ede2d321034e8517ea90baefb31831a8608afccc446d8a699fb1d00d4  /work/lib/httpcore-nio-4.4.16.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/mina/mina-http/2.2.10/mina-http-2.2.10.jar -o /work/lib/mina-http-2.2.10.jar \
    && echo '45d6c7f1ef59049f97973ef92e114bae1babb5d7789c52c6033a2213460898b4  /work/lib/mina-http-2.2.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar -o /work/lib/slf4j-api-1.7.36.jar \
    && echo 'd3ef575e3e4979678dc01bf1dcce51021493b4d11fb7f1be8ad982877c16a1c0  /work/lib/slf4j-api-1.7.36.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/mina/mina-core/2.2.10/mina-core-2.2.10.jar -o /work/lib/mina-core-2.2.10.jar \
    && echo 'db51dd8fedb86c0c3f181de036fe8ff876b3b6c98a30d169af7ee612b86fbf67  /work/lib/mina-core-2.2.10.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-nop/1.7.36/slf4j-nop-1.7.36.jar -o /work/lib/slf4j-nop-1.7.36.jar \
    && echo 'c214958b07816cb4412b30c7bdbd4308ffdc6ba2a83767b8f3a9229cbd9274d6  /work/lib/slf4j-nop-1.7.36.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/glassfish/grizzly/grizzly-http/5.0.3/grizzly-http-5.0.3.jar -o /work/lib/grizzly-http-5.0.3.jar \
    && echo '1e6fcc8cbf785bbef039c5e837979fb79b05a397aae77e540a4943e0bdfb6931  /work/lib/grizzly-http-5.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/glassfish/grizzly/grizzly-framework/5.0.3/grizzly-framework-5.0.3.jar -o /work/lib/grizzly-framework-5.0.3.jar \
    && echo '6738df4c11b7dbb44bb919984d92ab3a7886b7b7a22ddea65cc64c86bacb2e91  /work/lib/grizzly-framework-5.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jglobus/ssl-proxies/2.1.0/ssl-proxies-2.1.0.jar -o /work/lib/ssl-proxies-2.1.0.jar \
    && echo 'cbc5307bb468a67b1bd0f4ca0a775d5c894150e4bcfb40c2987ab191b3dd4cd2  /work/lib/ssl-proxies-2.1.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.1.1/commons-logging-1.1.1.jar -o /work/lib/commons-logging-1.1.1.jar \
    && echo 'ce6f913cad1f0db3aad70186d65c5bc7ffcc9a99e3fe8e0b137312819f7c362f  /work/lib/commons-logging-1.1.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/log4j/log4j/1.2.14/log4j-1.2.14.jar -o /work/lib/log4j-1.2.14.jar \
    && echo 'e3bff9ab64a09b1ac2800f3b5fb1e3d99728064acb6dd3924938507638a404fb  /work/lib/log4j-1.2.14.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk15on/1.50/bcprov-jdk15on-1.50.jar -o /work/lib/bcprov-jdk15on-1.50.jar \
    && echo '115b14a02b91fb03cb1866d6b311d33cd5518a9d8524dd63a14f19571e420404  /work/lib/bcprov-jdk15on-1.50.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/bottomless-archive-project/java-warc/1.2.1/java-warc-1.2.1.jar -o /work/lib/java-warc-1.2.1.jar \
    && echo '91e6755cc57ca304c3b953a61b8079bed01fd30cb5d9e2d27ffa768ac16cdd2b  /work/lib/java-warc-1.2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/22.0.0/annotations-22.0.0.jar -o /work/lib/annotations-22.0.0.jar \
    && echo '9f45f5d5184d50a777742389a7a6e6a5b0bf90b316919774d8336f94776c31b2  /work/lib/annotations-22.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-httpclient/commons-httpclient/3.1/commons-httpclient-3.1.jar -o /work/lib/commons-httpclient-3.1.jar \
    && echo 'dbd4953d013e10e7c1cc3701a3e6ccd8c950c892f08d804fabfac21705930443  /work/lib/commons-httpclient-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-codec-http/5.0.0.Alpha5/netty5-codec-http-5.0.0.Alpha5.jar -o /work/lib/netty5-codec-http-5.0.0.Alpha5.jar \
    && echo '65c0334ac55c7665049d39a17479901117fdd295805a449012425ff44d9d1cad  /work/lib/netty5-codec-http-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-common/5.0.0.Alpha5/netty5-common-5.0.0.Alpha5.jar -o /work/lib/netty5-common-5.0.0.Alpha5.jar \
    && echo '9282980912f6be5ebe4dc2e5218e4450e4562d99eed3d2bfac455cf2e9f82e14  /work/lib/netty5-common-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-buffer/5.0.0.Alpha5/netty5-buffer-5.0.0.Alpha5.jar -o /work/lib/netty5-buffer-5.0.0.Alpha5.jar \
    && echo '40b45fa57d593cfc88eb56849d495a881e972d6c0566908d667583fdabf36e50  /work/lib/netty5-buffer-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-transport/5.0.0.Alpha5/netty5-transport-5.0.0.Alpha5.jar -o /work/lib/netty5-transport-5.0.0.Alpha5.jar \
    && echo '72820bfe2c1a8934287cf77c71095b0e8c7ca84e744fe915821ca2ac1214de29  /work/lib/netty5-transport-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-resolver/5.0.0.Alpha5/netty5-resolver-5.0.0.Alpha5.jar -o /work/lib/netty5-resolver-5.0.0.Alpha5.jar \
    && echo 'c2b6d9c9b37f51fe8040f2d1389d898538c4158b0a7f40e52ae018e506e4d75b  /work/lib/netty5-resolver-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-codec/5.0.0.Alpha5/netty5-codec-5.0.0.Alpha5.jar -o /work/lib/netty5-codec-5.0.0.Alpha5.jar \
    && echo '2db51916c35fafa9c7da83cce513d3fa8891ededcd742d26199d0f4b7f38b3b2  /work/lib/netty5-codec-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-handler/5.0.0.Alpha5/netty5-handler-5.0.0.Alpha5.jar -o /work/lib/netty5-handler-5.0.0.Alpha5.jar \
    && echo '421d6ed05f91e7354d92d38ccaed8678d108aa587a17ced9a1c5910ef533e8ae  /work/lib/netty5-handler-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty5-transport-native-unix-common/5.0.0.Alpha5/netty5-transport-native-unix-common-5.0.0.Alpha5.jar -o /work/lib/netty5-transport-native-unix-common-5.0.0.Alpha5.jar \
    && echo '7845b96329b0eed7158b3b0c4b8d6dc6326d6d728c11cb8688b02a1512e84f60  /work/lib/netty5-transport-native-unix-common-5.0.0.Alpha5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty/3.10.6.Final/netty-3.10.6.Final.jar -o /work/lib/netty-3.10.6.Final.jar \
    && echo '8768a50fbe3d93a88d8e6000ea5d68e30f50dc915b3764c3c5870f70c4fb3b49  /work/lib/netty-3.10.6.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/eclipse/jetty/jetty-http/12.1.15/jetty-http-12.1.15.jar -o /work/lib/jetty-http-12.1.15.jar \
    && echo '641774717e2fa668ce3a8915c51ce1f4503037a1209620d7bbd074e70b23b7fd  /work/lib/jetty-http-12.1.15.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/eclipse/jetty/jetty-io/12.1.15/jetty-io-12.1.15.jar -o /work/lib/jetty-io-12.1.15.jar \
    && echo 'b5f940782fe61bb1b51269eba7cadd1afa771e2bd649e1fa48057d1647ec9212  /work/lib/jetty-io-12.1.15.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/eclipse/jetty/jetty-util/12.1.15/jetty-util-12.1.15.jar -o /work/lib/jetty-util-12.1.15.jar \
    && echo '74cb58a645f9d265d8e061b9227ec13c7acbb16c34bd6610eca229f58e928f37  /work/lib/jetty-util-12.1.15.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-codec-http/4.2.20.Final/netty-codec-http-4.2.20.Final.jar -o /work/lib/netty-codec-http-4.2.20.Final.jar \
    && echo 'd08b0d473c48c61ebb2bc4d145111fa1777832aee4d2be1024891e904e36eaf5  /work/lib/netty-codec-http-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-common/4.2.20.Final/netty-common-4.2.20.Final.jar -o /work/lib/netty-common-4.2.20.Final.jar \
    && echo '5807fef7eb619bc0a5d1c0e6c83199ea9bca8503203a3eb73cfdccec2d215743  /work/lib/netty-common-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-buffer/4.2.20.Final/netty-buffer-4.2.20.Final.jar -o /work/lib/netty-buffer-4.2.20.Final.jar \
    && echo '794136fc6be78e44a286c2b1420a182e135c6d06eb8c397030c1551ee50acccd  /work/lib/netty-buffer-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-transport/4.2.20.Final/netty-transport-4.2.20.Final.jar -o /work/lib/netty-transport-4.2.20.Final.jar \
    && echo 'ff4f1f8158c714c1b485ef10cf2456fbd3c1b2930256b70287aeb7dc3ad94783  /work/lib/netty-transport-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-resolver/4.2.20.Final/netty-resolver-4.2.20.Final.jar -o /work/lib/netty-resolver-4.2.20.Final.jar \
    && echo 'cb7a6027e4f366fb28dcea7e1f7088ca16bd23c2cc38e8ddfdac77a77bd144dc  /work/lib/netty-resolver-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-codec-base/4.2.20.Final/netty-codec-base-4.2.20.Final.jar -o /work/lib/netty-codec-base-4.2.20.Final.jar \
    && echo '5a66da26b86d7eecedd9e0d8fe0e22ef1733bbf873e476cb9b860afbed22210c  /work/lib/netty-codec-base-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-codec-compression/4.2.20.Final/netty-codec-compression-4.2.20.Final.jar -o /work/lib/netty-codec-compression-4.2.20.Final.jar \
    && echo '7ebae4ac80c01e2d279d0e50d377bcdaf0cf8f2f65797e0578afc810a66ab57d  /work/lib/netty-codec-compression-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-handler/4.2.20.Final/netty-handler-4.2.20.Final.jar -o /work/lib/netty-handler-4.2.20.Final.jar \
    && echo '211dbbba074298046b37f841ad9ca89ed91968f6b9e97400c99ab4e6177b1f96  /work/lib/netty-handler-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/netty/netty-transport-native-unix-common/4.2.20.Final/netty-transport-native-unix-common-4.2.20.Final.jar -o /work/lib/netty-transport-native-unix-common-4.2.20.Final.jar \
    && echo '6f600d5cbd3ce39e50680de66b00d7e6a9652dac7d08a5b022101d717cb7fb52  /work/lib/netty-transport-native-unix-common-4.2.20.Final.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/http/http1_1-parser/2.1.109/http1_1-parser-2.1.109.jar -o /work/lib/http1_1-parser-2.1.109.jar \
    && echo 'a12bfe9514011e3eb9c16d386405fb2fd7018aa7c43a2507bd61911b2bcc2ed1  /work/lib/http1_1-parser-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/core/core-datawrapper/2.1.109/core-datawrapper-2.1.109.jar -o /work/lib/core-datawrapper-2.1.109.jar \
    && echo '044799f604a46e961b013659575def5df8b4e5460dfd5fd0d7ea309cc5900c70  /work/lib/core-datawrapper-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/core/core-util/2.1.109/core-util-2.1.109.jar -o /work/lib/core-util-2.1.109.jar \
    && echo 'c6f53207cddf7da4b841f215e87396865bb733732f2a51dc8de8c9636faf4a82  /work/lib/core-util-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jakarta/inject/jakarta.inject-api/1.0.5/jakarta.inject-api-1.0.5.jar -o /work/lib/jakarta.inject-api-1.0.5.jar \
    && echo 'a852b0971c589491e24334bd77e92760c048d2c102fc4c68e582e1cd53130f84  /work/lib/jakarta.inject-api-1.0.5.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/core/core-future/2.1.109/core-future-2.1.109.jar -o /work/lib/core-future-2.1.109.jar \
    && echo '1d451106bdffc577721cf0a0a3dfacccaad3b2c528441d48fe96ba7d158ebf26  /work/lib/core-future-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/core/core-metrics/2.1.109/core-metrics-2.1.109.jar -o /work/lib/core-metrics-2.1.109.jar \
    && echo '5396239da6c3c4d0a86c9eaa19572e8689595dc49e2e3a108b1c9e7111478660  /work/lib/core-metrics-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/micrometer/micrometer-core/1.9.4/micrometer-core-1.9.4.jar -o /work/lib/micrometer-core-1.9.4.jar \
    && echo '8b0a72216589e52ef1c5baeebe93a1164c9f3a9f8c968bd906a211ab70e8ecb8  /work/lib/micrometer-core-1.9.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/hdrhistogram/HdrHistogram/2.1.12/HdrHistogram-2.1.12.jar -o /work/lib/HdrHistogram-2.1.12.jar \
    && echo '9b47fbae444feaac4b7e04f0ea294569e4bc282bc69d8c2ce2ac3f23577281e2  /work/lib/HdrHistogram-2.1.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/latencyutils/LatencyUtils/2.0.3/LatencyUtils-2.0.3.jar -o /work/lib/LatencyUtils-2.0.3.jar \
    && echo 'a32a9ffa06b2f4e01c5360f8f9df7bc5d9454a5d373cd8f361347fa5a57165ec  /work/lib/LatencyUtils-2.0.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/webpieces/core/core-logging/2.1.109/core-logging-2.1.109.jar -o /work/lib/core-logging-2.1.109.jar \
    && echo '348e2e5132534e4f16fe7dbad8fb428625e699d9a7e89bc8420e8a783e7b189a  /work/lib/core-logging-2.1.109.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ch/qos/logback/logback-classic/1.4.8/logback-classic-1.4.8.jar -o /work/lib/logback-classic-1.4.8.jar \
    && echo 'e6d9c1208bf664c427b9f5fe970b8372f794247473693c3f5d2440fa6b7bb527  /work/lib/logback-classic-1.4.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ch/qos/logback/logback-core/1.4.8/logback-core-1.4.8.jar -o /work/lib/logback-core-1.4.8.jar \
    && echo '123453142b41b627bc0d035d1fee8c1ed4deafacfbdacbe3a238934c19a0627a  /work/lib/logback-core-1.4.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/httpcomponents/core5/httpcore5/5.4.4/httpcore5-5.4.4.jar -o /work/lib/httpcore5-5.4.4.jar \
    && echo 'b08e3c3a440fec2029e89980134c7c787dd6796454641ad1eafb81478d7e8b0b  /work/lib/httpcore5-5.4.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/httpcomponents/httpcore/4.4.16/httpcore-4.4.16.jar -o /work/lib/httpcore-4.4.16.jar \
    && echo '6c9b3dd142a09dc468e23ad39aad6f75a0f2b85125104469f026e52a474e464f  /work/lib/httpcore-4.4.16.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/netpreserve/commons/webarchive-commons/3.0.5/webarchive-commons-3.0.5-sources.jar -o /work/parser-sources.jar \
    && echo 'd81fecd132712248c03a2f072fd5f79a37d3739adbb3e7b9c91e8f5afe396b60  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Http11Adapter.java GenericHarness.java /work/src/
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
