FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Only Xerces classes go on the class path: the xml-apis dependency duplicates
# packages that the java.xml module already exports, and xml-resolver is only
# used for catalog resolution. Both are pinned here as compile-only inputs.
RUN mkdir /work/deps \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xerces/xercesImpl/2.12.2/xercesImpl-2.12.2.jar -o /work/deps/xercesImpl-2.12.2.jar \
    && echo '6fc991829af1708d15aea50c66f0beadcd2cfeb6968e0b2f55c1b0909883fe16  /work/deps/xercesImpl-2.12.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-apis/xml-apis/1.4.01/xml-apis-1.4.01.jar -o /work/deps/xml-apis-1.4.01.jar \
    && echo 'a840968176645684bb01aed376e067ab39614885f9eee44abe35a5f20ebe7fad  /work/deps/xml-apis-1.4.01.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xml-resolver/xml-resolver/1.2/xml-resolver-1.2.jar -o /work/deps/xml-resolver-1.2.jar \
    && echo '47dcde8986019314ef78ae7280a94973a21d2ed95075a40a000b42da956429e1  /work/deps/xml-resolver-1.2.jar' | sha256sum --check
# Coverage subject: the Xerces2-J scanner, DOM builder and namespace binder.
# The release jar is compiled without line-number tables, so the pinned sources
# jar for the same release is recompiled with -g and laid over the unpacked
# release jar, which keeps its message bundles, service files and the html/wml
# DOM classes that are not recompiled.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xerces/xercesImpl/2.12.2/xercesImpl-2.12.2-sources.jar -o /work/parser-sources.jar \
    && echo '3c531edfc074e3e0885e5d4a777a9e7317e108028be50ef6e893a5a9cf3e12c2  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes /work/lib \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && find /work/parser-source/org/apache/xerces -name '*.java' > /work/xerces-sources.txt \
    && javac -nowarn -g -encoding ISO-8859-1 --release 8 -sourcepath /work/parser-source \
       -cp /work/deps/xml-resolver-1.2.jar:/work/deps/xml-apis-1.4.01.jar \
       -d /work/parser-classes @/work/xerces-sources.txt 2>/dev/null \
    && mkdir /work/lib/xerces \
    && unzip -q /work/deps/xercesImpl-2.12.2.jar -d /work/lib/xerces -x 'META-INF/MANIFEST.MF' \
    && cp -a /work/parser-classes/. /work/lib/xerces/ \
    && rm -rf /work/parser-classes/org/apache/xml /work/parser-classes/org/apache/html /work/parser-classes/org/apache/wml
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY XmlAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp /work/lib/xerces -d /work/classes /work/src/*.java \
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
