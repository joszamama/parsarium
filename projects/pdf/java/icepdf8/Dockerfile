FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/pcorless/icepdf/icepdf-core/8.0.0/icepdf-core-8.0.0.jar -o /work/lib/icepdf-core-8.0.0.jar \
    && echo 'fb496db1f0fd7d4441dc6fe79e19bb8b871890edac66e7d80ba2ec64ed7088b3  /work/lib/icepdf-core-8.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/pcorless/icepdf/icepdf-fonts/8.0.0/icepdf-fonts-8.0.0.jar -o /work/lib/icepdf-fonts-8.0.0.jar \
    && echo '45542cfb82065d50505562b3841cf4f018a6889766bbfc09d1be1682c41f67d6  /work/lib/icepdf-fonts-8.0.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcprov-jdk18on/1.86/bcprov-jdk18on-1.86.jar -o /work/lib/bcprov-jdk18on-1.86.jar \
    && echo '2af190b300cbb0b35e248ccf5f4a06b6072030aeb3da7a98ec73abe5b4cb371f  /work/lib/bcprov-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcpkix-jdk18on/1.86/bcpkix-jdk18on-1.86.jar -o /work/lib/bcpkix-jdk18on-1.86.jar \
    && echo '8d8b41a4b149bdae8d331f059a578870954d1e3ff29f8269a9eb3ee19a7e4ef7  /work/lib/bcpkix-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/bouncycastle/bcutil-jdk18on/1.86/bcutil-jdk18on-1.86.jar -o /work/lib/bcutil-jdk18on-1.86.jar \
    && echo '1c268e15f785aafb1e4670d8d6e5f856f69475e96c162dadcd1ff9b350e9139f  /work/lib/bcutil-jdk18on-1.86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/fontbox/3.0.8/fontbox-3.0.8.jar -o /work/lib/fontbox-3.0.8.jar \
    && echo 'a1915c24e3edbe0ecec93896dfbf6d41427810b663ade97bd4e8bae86ec3fdab  /work/lib/fontbox-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/pdfbox-io/3.0.8/pdfbox-io-3.0.8.jar -o /work/lib/pdfbox-io-3.0.8.jar \
    && echo '36a0e04001010b4c764857817412b96339930b19755e728959805cc0352061b2  /work/lib/pdfbox-io-3.0.8.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.4.0/commons-logging-1.4.0.jar -o /work/lib/commons-logging-1.4.0.jar \
    && echo 'd175dbd751dd782a63bde28c7a039520e971f25e84b79c19b8435edc3603e0dc  /work/lib/commons-logging-1.4.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/pdfbox/jbig2-imageio/3.0.4/jbig2-imageio-3.0.4.jar -o /work/lib/jbig2-imageio-3.0.4.jar \
    && echo '29cb2951622f10acf61fd0656c4e6fa5562194a9095f7a1d26aa426e2f6b17eb  /work/lib/jbig2-imageio-3.0.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/pcorless/jpx-imageio/0.1.0/jpx-imageio-0.1.0.jar -o /work/lib/jpx-imageio-0.1.0.jar \
    && echo 'aa0db096b431de2c4398866228537c2b3db466cb09c7b7879cf009953bee9df0  /work/lib/jpx-imageio-0.1.0.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/pcorless/icepdf/icepdf-core/8.0.0/icepdf-core-8.0.0-sources.jar -o /work/parser-sources.jar \
    && echo 'c34658d0dbc3feb5abbb634461f50fc80e183d6856498446073e79fae22123da  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY IcePdf8Adapter.java GenericHarness.java /work/src/
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
