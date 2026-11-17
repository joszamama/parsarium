FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# pcap4j-core 1.8.2 with its documented runtime packet-factory module (pcap4j-packetfactory-static,
# which supplies the DNS RDATA factories) and the two compile dependencies pinned by the parent POM:
# jna 5.3.1 (never loaded natively here; no capture handle is opened) and slf4j-api 1.7.26.
RUN mkdir /work/lib && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/pcap4j/pcap4j-core/1.8.2/pcap4j-core-1.8.2.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/pcap4j/pcap4j-packetfactory-static/1.8.2/pcap4j-packetfactory-static-1.8.2.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/net/java/dev/jna/jna/5.3.1/jna-5.3.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.26/slf4j-api-1.7.26.jar \
    && curl --fail --location --retry 3 -o /work/pcap4j-1.8.2.pom https://repo.maven.apache.org/maven2/org/pcap4j/pcap4j/1.8.2/pcap4j-1.8.2.pom \
    && printf '%s\n' \
       '3153208d0212ed818705802fe44e851aec5063a4527075a66043f71c7363160a  pcap4j-core-1.8.2.jar' \
       '5946006b70d5811cbef1e5808f8d51b4f22a725fecb48274b87a668d3c9b1237  pcap4j-packetfactory-static-1.8.2.jar' \
       '01cb505c0698d0f7acf3524c7e73acb7dc424a5bae5e9c86ce44075ab32bc4ee  jna-5.3.1.jar' \
       '6d9e5b86cfd1dd44c676899285b5bb4fa0d371cf583e8164f9c8a0366553242b  slf4j-api-1.7.26.jar' \
       'a53d00da01e45e4130f3eb5c837ed0fde210cc671331ae314a69c6ad6b981a62  /work/pcap4j-1.8.2.pom' \
       | sha256sum --check \
    && grep -q '<name>MIT License</name>' /work/pcap4j-1.8.2.pom
# Coverage subject: org.pcap4j from both pinned source jars (DnsPacket, DnsDomainName, DnsResourceRecord,
# DnsRData* and the static RDATA factory).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/pcap4j/pcap4j-core/1.8.2/pcap4j-core-1.8.2-sources.jar -o /work/core-sources.jar \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/pcap4j/pcap4j-packetfactory-static/1.8.2/pcap4j-packetfactory-static-1.8.2-sources.jar -o /work/static-sources.jar \
    && printf '%s\n' \
       '270e89c1c4d32599ab2046f19e9977d56b51afdd402c06f4743d72cbfe88a17d  /work/core-sources.jar' \
       'd30fb990d18a7850b2037a9df1162fbe0e7bec76d89bc9e9f7a315941830e7dd  /work/static-sources.jar' \
       | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/core-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -qo /work/static-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/pcap4j-core-1.8.2.jar -d /work/parser-classes -x 'META-INF/*' \
    && unzip -qo /work/lib/pcap4j-packetfactory-static-1.8.2.jar -d /work/parser-classes -x 'META-INF/*'
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY Pcap4jDnsHarness.java /work/src/
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
