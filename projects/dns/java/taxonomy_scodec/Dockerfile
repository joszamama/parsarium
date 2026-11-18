FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# taxonomy-scodec_2.13 1.0.0 (DnsCodec, the wire decoder), taxonomy-model_2.13 1.0.0 (its DnsMessage model) and the
# compile-scope dependencies their POMs name: scodec-core 1.11.7 (scodec-bits 1.1.14, shapeless 2.3.3), enumeratum
# 1.6.1 (enumeratum-macros 1.6.1) and scala-library 2.13.5. The fs2 module (taxonomy-fs2, the network client) is not used.
RUN mkdir /work/lib && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/fr/davit/taxonomy-scodec_2.13/1.0.0/taxonomy-scodec_2.13-1.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/fr/davit/taxonomy-model_2.13/1.0.0/taxonomy-model_2.13-1.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scodec/scodec-core_2.13/1.11.7/scodec-core_2.13-1.11.7.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scodec/scodec-bits_2.13/1.1.14/scodec-bits_2.13-1.1.14.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/chuusai/shapeless_2.13/2.3.3/shapeless_2.13-2.3.3.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/beachape/enumeratum_2.13/1.6.1/enumeratum_2.13-1.6.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/beachape/enumeratum-macros_2.13/1.6.1/enumeratum-macros_2.13-1.6.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.5/scala-library-2.13.5.jar \
    && curl --fail --location --retry 3 -o /work/taxonomy-scodec_2.13-1.0.0.pom https://repo.maven.apache.org/maven2/fr/davit/taxonomy-scodec_2.13/1.0.0/taxonomy-scodec_2.13-1.0.0.pom \
    && curl --fail --location --retry 3 -o /work/taxonomy-model_2.13-1.0.0.pom https://repo.maven.apache.org/maven2/fr/davit/taxonomy-model_2.13/1.0.0/taxonomy-model_2.13-1.0.0.pom \
    && printf '%s\n' \
       'd2edeacdaa1224f5a727ba5b26cde466fc81970ea53b56a806207ebd94cb7cde  taxonomy-scodec_2.13-1.0.0.jar' \
       '1fb114cf942a71b797936a5c2cd569eeb0162da9184775b1691d3ebcce06f1b2  taxonomy-model_2.13-1.0.0.jar' \
       '4f9f27d0cdb18825b4ce693f785e032d6ee16225491116d20f43ad39eede0236  scodec-core_2.13-1.11.7.jar' \
       '231e59203209ef34eb4e8ab6279d95393a37e5035405eb9451a320715ca4ebe9  scodec-bits_2.13-1.1.14.jar' \
       '1569de6437d71e878807302f8e1b06a06b62d217cd4a30e8019c9543d6683dff  shapeless_2.13-2.3.3.jar' \
       'b9dfeed4b3d59009f0886cce331c067edc18ced5229e78ab088decc6fdeb54cf  enumeratum_2.13-1.6.1.jar' \
       '39d7387df991b206fdfdee93de8d705f1736db03c4ffd845ed8577074823b7f5  enumeratum-macros_2.13-1.6.1.jar' \
       '52aafeef8e0d104433329b1bc31463d1b4a9e2b8f24f85432c8cfaed9fad2587  scala-library-2.13.5.jar' \
       '2a5a7ba7b0714fe51aba4be244a68d4987b70b1a33e7eec92e324c755f19aad4  /work/taxonomy-scodec_2.13-1.0.0.pom' \
       '64e86b0ccfd5f8638423d110dcc5e6101fe612f150537bde74d64eceef3f05c1  /work/taxonomy-model_2.13-1.0.0.pom' \
       | sha256sum --check \
    && grep -q '<name>Apache-2.0</name>' /work/taxonomy-scodec_2.13-1.0.0.pom \
    && grep -q '<name>Apache-2.0</name>' /work/taxonomy-model_2.13-1.0.0.pom \
    && grep -q '<artifactId>scodec-core_2.13</artifactId>' /work/taxonomy-scodec_2.13-1.0.0.pom \
    && grep -q '<artifactId>enumeratum_2.13</artifactId>' /work/taxonomy-model_2.13-1.0.0.pom
# Coverage subject: fr.davit.taxonomy (scodec/DnsCodec.scala and the model classes it builds).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/fr/davit/taxonomy-scodec_2.13/1.0.0/taxonomy-scodec_2.13-1.0.0-sources.jar -o /work/scodec-sources.jar \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/fr/davit/taxonomy-model_2.13/1.0.0/taxonomy-model_2.13-1.0.0-sources.jar -o /work/model-sources.jar \
    && printf '%s\n' \
       'c99db51feb2bb2cb3b88509e4f02e7efb7399c3c07983f7306aafba21071b65b  /work/scodec-sources.jar' \
       'eb82bb0ce06fd5f0748e6b6801a42e48563045d57eec97763adc4a74d03e2986  /work/model-sources.jar' \
       | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/scodec-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q -o /work/model-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/taxonomy-scodec_2.13-1.0.0.jar -d /work/parser-classes -x 'META-INF/*' \
    && unzip -q -o /work/lib/taxonomy-model_2.13-1.0.0.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY TaxonomyHarness.java /work/src/
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
