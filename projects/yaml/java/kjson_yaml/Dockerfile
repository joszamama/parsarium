FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-yaml/3.15/kjson-yaml-3.15.jar -o /work/lib/kjson-yaml-3.15.jar \
    && echo 'ad626d11e60a22f06207f3df3f5746f25a49b77841eeed3fe7faa96822d14bc7  /work/lib/kjson-yaml-3.15.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-core/10.2/kjson-core-10.2.jar -o /work/lib/kjson-core-10.2.jar \
    && echo '1f0bc7d86bda795c5e3bd713f234b2323efe4fb138c5a6549b87c6662f6560b9  /work/lib/kjson-core-10.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-exception/1.3/kjson-exception-1.3.jar -o /work/lib/kjson-exception-1.3.jar \
    && echo 'b542f67688536802371c543627fb4e2cf01821f1d5f48dfe9b79ec3faf6c3396  /work/lib/kjson-exception-1.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/json-functions/2.1/json-functions-2.1.jar -o /work/lib/json-functions-2.1.jar \
    && echo 'ef3df4bdc148233b9ae7ff2f4e6d427552c6580b22a2aa975678cb292c38d47f  /work/lib/json-functions-2.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kstuff/json-co-functions/2.0/json-co-functions-2.0.jar -o /work/lib/json-co-functions-2.0.jar \
    && echo '931e7431729bb101d9a87f522bbe7991441d66b68644c7b580d5ccbd8e894142  /work/lib/json-co-functions-2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/int-output/3.0/int-output-3.0.jar -o /work/lib/int-output-3.0.jar \
    && echo '50b355d2d4b050761088e79ecfc506c999fa3caaf4d9935d77c8baaaaf0250f7  /work/lib/int-output-3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kstuff/co-int-output/3.0/co-int-output-3.0.jar -o /work/lib/co-int-output-3.0.jar \
    && echo '85830aedd6376b37e7cf4c638c98df559c409f78c1ce60c7824a90695920e45c  /work/lib/co-int-output-3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/immutables/3.0/immutables-3.0.jar -o /work/lib/immutables-3.0.jar \
    && echo 'd08b7b58911b909206e95b88762067e177413c623b15d748720227c936b21b07  /work/lib/immutables-3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-pointer/8.12/kjson-pointer-8.12.jar -o /work/lib/kjson-pointer-8.12.jar \
    && echo '17c785462910bdb5a3d2044afc2bfd2614539e55657c2b8ae65848662b310f7c  /work/lib/kjson-pointer-8.12.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-pointer-core/1.4/kjson-pointer-core-1.4.jar -o /work/lib/kjson-pointer-core-1.4.jar \
    && echo 'd940a016d0ccc6860fe46fd5c6a506281af67cf1db10c14e85e6576d87f99cfe  /work/lib/kjson-pointer-core-1.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/textmatcher/3.1/textmatcher-3.1.jar -o /work/lib/textmatcher-3.1.jar \
    && echo '26bee868ff7fa660238101a6a8572dc9fa354203f35ffbccbd763a026f73494f  /work/lib/textmatcher-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kstuff/string-mapper/3.1/string-mapper-3.1.jar -o /work/lib/string-mapper-3.1.jar \
    && echo '44b10b64169c6d7c51dc80d278d304ca40bb0db93777868bcde8339aa408b1a4  /work/lib/string-mapper-3.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/pipelines/7.0/pipelines-7.0.jar -o /work/lib/pipelines-7.0.jar \
    && echo '3d52e250ecae54784bc5482a7c4fb8d56483381b28bd9e45be70b1dc659c6ad2  /work/lib/pipelines-7.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kstuff/log-front-kotlin/7.0/log-front-kotlin-7.0.jar -o /work/lib/log-front-kotlin-7.0.jar \
    && echo 'ba83a64ea6e89d40c99cb0de3e59d4e48c3f90710eec9fc55a7f848bd73a6cfc  /work/lib/log-front-kotlin-7.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/log-front/7.0/log-front-7.0.jar -o /work/lib/log-front-7.0.jar \
    && echo '54ff29858730147c1ac9740589d107ea54bb59915f39ffae83899f3aacb08829  /work/lib/log-front-7.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/jstuff/log-front-api/3.0/log-front-api-3.0.jar -o /work/lib/log-front-api-3.0.jar \
    && echo 'df10578b3e1b95ebca2d5cdf0b3ab15482e71a594d37bb13e1ec9027c359b2fa  /work/lib/log-front-api-3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-coroutines-core/1.9.0/kotlinx-coroutines-core-1.9.0.jar -o /work/lib/kotlinx-coroutines-core-1.9.0.jar \
    && echo '7089c33c145865020760d3dbca5e4634133cc3dd7feb926e830f6de6ede28ac6  /work/lib/kotlinx-coroutines-core-1.9.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-coroutines-core-jvm/1.9.0/kotlinx-coroutines-core-jvm-1.9.0.jar -o /work/lib/kotlinx-coroutines-core-jvm-1.9.0.jar \
    && echo 'ad89c2892235e670f222d819cb3d81188143cb19a05b59df9889ae4269f5c70a  /work/lib/kotlinx-coroutines-core-jvm-1.9.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk8/2.0.21/kotlin-stdlib-jdk8-2.0.21.jar -o /work/lib/kotlin-stdlib-jdk8-2.0.21.jar \
    && echo '15c8c0acb311483c068d1697501965474b70dfd80ac79580eca3a03cf51e4a1d  /work/lib/kotlin-stdlib-jdk8-2.0.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.0.21/kotlin-stdlib-2.0.21.jar -o /work/lib/kotlin-stdlib-2.0.21.jar \
    && echo 'f31cc53f105a7e48c093683bbd5437561d1233920513774b470805641bedbc09  /work/lib/kotlin-stdlib-2.0.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar -o /work/lib/annotations-13.0.jar \
    && echo 'ace2a10dc8e2d5fd34925ecac03e4988b2c0f851650c94b8cef49ba1bd111478  /work/lib/annotations-13.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk7/2.0.21/kotlin-stdlib-jdk7-2.0.21.jar -o /work/lib/kotlin-stdlib-jdk7-2.0.21.jar \
    && echo '712f480760edeee48a84369e6be89f6ab52375408bb2ca3be14ef663f72bee31  /work/lib/kotlin-stdlib-jdk7-2.0.21.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-yaml/3.15/kjson-yaml-3.15-sources.jar -o /work/parser-sources.jar \
    && echo '32cf4cb8945acb0ce0986bb4993df41e6fbd351ecdbacab66a2cd11cb43c05d2  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/kjson/kjson-yaml/3.15/kjson-yaml-3.15.pom -o /work/parser.pom \
    && echo 'd6ac021fcbc6f5926c7ca81cb00a238d68964e187969a68f14bb17cb6306c912  /work/parser.pom' | sha256sum --check \
    && grep -q '<name>The MIT License (MIT)</name>' /work/parser.pom \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/kjson-yaml-3.15.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY YamlAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
