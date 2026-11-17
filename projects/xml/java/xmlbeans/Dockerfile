FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Coverage subjects: XMLBeans 5.4.1 tree/SAX loader and the underlying
# java.xml internal Xerces fork. Their pinned sources are kept separate.
RUN echo 'fdbf1d201a93f5438aed3e4d101788da4ca05f82320d8a11336ced86edebb1ef  /opt/java/openjdk/lib/modules' | sha256sum --check \
    && jimage extract --dir /work/jdk-module --include 'regex:/java.xml/.*' /opt/java/openjdk/lib/modules \
    && mkdir -p /work/lib /work/parser-classes/com/sun/org/apache /work/parser-classes/javax/xml \
    && cp -a /work/jdk-module/java.xml/com/sun/org/apache/xerces /work/parser-classes/com/sun/org/apache/xerces \
    && cp -a /work/jdk-module/java.xml/javax/xml/parsers /work/parser-classes/javax/xml/parsers
RUN curl --fail --location --retry 3 https://github.com/openjdk/jdk25u/archive/refs/tags/jdk-25.0.5+8.tar.gz -o /work/jdk25u.tar.gz \
    && echo 'e4cc23905feaec9d91033262d4f36a2932e145f80ed66638d61ab522f89ed8b1  /work/jdk25u.tar.gz' | sha256sum --check \
    && mkdir -p /work/parser-source/underlying /work/parser-source/module \
    && tar -xzf /work/jdk25u.tar.gz -C /work/parser-source/underlying --strip-components=5 \
       jdk25u-jdk-25.0.5-8/src/java.xml/share/classes/com/sun/org/apache/xerces \
       jdk25u-jdk-25.0.5-8/src/java.xml/share/classes/javax/xml/parsers \
    && rm /work/jdk25u.tar.gz
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlbeans/xmlbeans/5.4.1/xmlbeans-5.4.1.jar -o /work/lib/xmlbeans-5.4.1.jar \
    && echo 'b8fe946b41983e86496a7a68508af82a41daafd0e2a2cc8c9302c53fcbd9802c  /work/lib/xmlbeans-5.4.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/xmlbeans/xmlbeans/5.4.1/xmlbeans-5.4.1-sources.jar -o /work/xmlbeans-sources.jar \
    && echo 'd50cbd466adec89811bc5797325e09279e3894387db59434dd99322ff774ee70  /work/xmlbeans-sources.jar' | sha256sum --check \
    && unzip -q /work/xmlbeans-sources.jar -d /work/parser-source/module -x 'META-INF/*' \
    && mkdir /work/module-classes \
    && unzip -q /work/lib/xmlbeans-5.4.1.jar -d /work/module-classes -x 'META-INF/*' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.26.1/log4j-api-2.26.1.jar -o /work/lib/log4j-api-2.26.1.jar \
    && echo 'f1810a4704ccce019d02bba029dc02a4f2ac0c997f647b465e7d409c1927f822  /work/lib/log4j-api-2.26.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.26.1/log4j-core-2.26.1.jar -o /work/lib/log4j-core-2.26.1.jar \
    && echo '2ec8c3bf5a6d7c89be8620116a2fc973f7dda1ad0261ad393c4d4726edfd3dcb  /work/lib/log4j-core-2.26.1.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY XmlAdapter.java GenericHarness.java /work/src/
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
COPY --from=build /work/module-classes /work/module-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
