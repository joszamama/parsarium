FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# XOM's release JAR has no line-number table. Compile the pinned same-release
# sources with debug lines; keep the published release JAR in the runtime image.
# Apache Xerces is a compile-only dependency so Builder selects the JDK fork.
RUN mkdir /work/lib /work/build-libs /work/parser-source /work/parser-classes \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xom/xom/1.4.6/xom-1.4.6.jar -o /work/lib/xom-1.4.6.jar \
    && echo 'e7f0aa3ebe81ed2a777091d688a3e32aad03225c74bda6fbbafeb9725cbb3fea  /work/lib/xom-1.4.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xom/xom/1.4.6/xom-1.4.6-sources.jar -o /work/parser-sources.jar \
    && echo 'e5ab760efd9d53a9f3ffbbea07a67dd7a64cb5cf79425d1f4223833370b124ac  /work/parser-sources.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/jaxen/jaxen/2.0.6/jaxen-2.0.6.jar -o /work/lib/jaxen-2.0.6.jar \
    && echo '3e2a755b283fd492fa4be204294c7abb7cd63ac94fb366baab9c7bb9afb00b6d  /work/lib/jaxen-2.0.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/xerces/xercesImpl/2.12.2/xercesImpl-2.12.2.jar -o /work/build-libs/xerces.jar \
    && echo '6fc991829af1708d15aea50c66f0beadcd2cfeb6968e0b2f55c1b0909883fe16  /work/build-libs/xerces.jar' | sha256sum --check \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*'
RUN javac -g --release 8 -Xlint:-options \
      -cp /work/lib/xom-1.4.6.jar:/work/lib/jaxen-2.0.6.jar:/work/build-libs/xerces.jar \
      -d /work/parser-classes $(find /work/parser-source/nu/xom -maxdepth 1 -name '*.java')
# Builder.findParser selects the JDK java.xml internal Xerces fork when the
# optional external Xerces classes are absent. Pin its modules and sources.
RUN echo 'fdbf1d201a93f5438aed3e4d101788da4ca05f82320d8a11336ced86edebb1ef  /opt/java/openjdk/lib/modules' | sha256sum --check \
    && jimage extract --dir /work/jdk-module --include 'regex:/java.xml/com/sun/org/apache/xerces/.*' /opt/java/openjdk/lib/modules \
    && mkdir -p /work/underlying-classes/com/sun/org/apache \
    && cp -a /work/jdk-module/java.xml/com/sun/org/apache/xerces /work/underlying-classes/com/sun/org/apache/xerces \
    && rm -rf /work/jdk-module
RUN curl --fail --location --retry 3 https://github.com/openjdk/jdk25u/archive/refs/tags/jdk-25.0.5+8.tar.gz -o /work/jdk25u.tar.gz \
    && echo 'e4cc23905feaec9d91033262d4f36a2932e145f80ed66638d61ab522f89ed8b1  /work/jdk25u.tar.gz' | sha256sum --check \
    && mkdir /work/underlying-source \
    && tar -xzf /work/jdk25u.tar.gz -C /work/underlying-source --strip-components=5 \
       jdk25u-jdk-25.0.5-8/src/java.xml/share/classes/com/sun/org/apache/xerces \
    && rm /work/jdk25u.tar.gz
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY XmlAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp /work/parser-classes:/work/lib/xom-1.4.6.jar:/work/lib/jaxen-2.0.6.jar \
      -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/underlying-source /work/underlying-source
COPY --from=build /work/underlying-classes /work/underlying-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
