FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Parser subject: the pinned dom4j 2.2.0 release jar and its same-release sources.
# Its POM dependencies (jaxen, xsdlib, jakarta.xml.bind-api, pull-parser, xpp3)
# are all optional and are not installed; SAXReader needs none of them.
RUN mkdir /work/lib /work/parser-source \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/dom4j/dom4j/2.2.0/dom4j-2.2.0.jar -o /work/lib/dom4j-2.2.0.jar \
    && echo '3fae79e081096e1410645eb3557c63b79ca266d510ab479889511109becd1690  /work/lib/dom4j-2.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/dom4j/dom4j/2.2.0/dom4j-2.2.0-sources.jar -o /work/parser-sources.jar \
    && echo 'e5b0a1fdd14bf61ea78a41eff7d6777abb602f480483e59897c3a3e247973187  /work/parser-sources.jar' | sha256sum --check \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*'
# Underlying tokenizer: SAXReader asks JAXP SAXParserFactory.newInstance() for a
# reader; with no factory configured that is this runtime's java.xml internal
# Xerces fork. Classes come from the pinned module image, sources from the
# matching OpenJDK jdk25u release tag.
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
RUN mkdir /work/classes && javac -cp /work/lib/dom4j-2.2.0.jar -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/underlying-source /work/underlying-source
COPY --from=build /work/underlying-classes /work/underlying-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
