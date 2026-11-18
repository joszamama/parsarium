FROM --platform=linux/amd64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    binutils bzip2 ca-certificates clang cmake curl libclang-rt-18-dev llvm ninja-build python3 unzip \
    libcurl4-openssl-dev libgdal-dev libgeotiff-dev liblzma-dev libproj-dev libxml2-dev libzstd-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# io.pdal:pdal_2.13 2.10.0 (Scala 2.13 JVM API, callable from Java), its runtime POM closure,
# and io.pdal:pdal-native 2.10.0 (JNI glue; the jar carries x86_64-linux and arm64-darwin only).
RUN mkdir /work/lib /work/stock-jars && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/io/pdal/pdal_2.13/2.10.0/pdal_2.13-2.10.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.16/scala-library-2.13.16.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/github/sbt/sbt-jni-core_2.13/1.7.0/sbt-jni-core_2.13-1.7.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/io/pdal/pdal-native/2.10.0/pdal-native-2.10.0.jar \
    && printf '%s\n' \
       '0ce4f834f2bb435ef8b26d8f5cc07a87418618746941f6d83d1da26653ac677b  pdal_2.13-2.10.0.jar' \
       '1ebb2b6f9e4eb4022497c19b1e1e825019c08514f962aaac197145f88ed730f1  scala-library-2.13.16.jar' \
       'c681cec01d0ca22a47369f370f054fa1ecc03cd30688c69008b330b86e2b10c9  sbt-jni-core_2.13-1.7.0.jar' \
       '8690bffe5fff8a28cc35e42d8203cba6406ee0b93bb2c067fec091333a5f2754  pdal-native-2.10.0.jar' \
       | sha256sum --check
RUN curl --fail --location --retry 3 -o /work/pdal_2.13-2.10.0.pom https://repo.maven.apache.org/maven2/io/pdal/pdal_2.13/2.10.0/pdal_2.13-2.10.0.pom \
    && echo 'feeffe9648bb91b004335107c519fbeb255fac44f50a2259bea29ff95920240e  /work/pdal_2.13-2.10.0.pom' | sha256sum --check \
    && mkdir /work/jni && unzip -q -j /work/lib/pdal-native-2.10.0.jar 'native/x86_64-linux/libpdaljni.2.10.so' -d /work/jni
# Coverage subjects: the pdal_2.13 Scala sources (JaCoCo) and the PDAL 2.10.2 release source
# (LLVM), whose io/PlyReader.cpp implements readers.ply.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/io/pdal/pdal_2.13/2.10.0/pdal_2.13-2.10.0-sources.jar -o /work/parser-sources.jar \
    && echo '34e5c0e3ad3ccc6aa1d9151f5c1dca7c71e24226d9c08754c3a1f4712031b6af  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && test -f /work/parser-source/io/pdal/Pipeline.scala \
    && curl --fail --location --retry 3 https://github.com/PDAL/PDAL/releases/download/2.10.2/PDAL-2.10.2-src.tar.bz2 -o /work/PDAL-2.10.2-src.tar.bz2 \
    && echo '882b97aa3ae5db682c3b2dc8edef4e29bcc7ecea51c70592e71bc1f34112ad00  /work/PDAL-2.10.2-src.tar.bz2' | sha256sum --check \
    && mkdir /work/source && tar -xjf /work/PDAL-2.10.2-src.tar.bz2 -C /work/source --strip-components=1 \
    && rm /work/PDAL-2.10.2-src.tar.bz2 \
    && test -f /work/source/io/PlyReader.cpp && test -f /work/source/LICENSE.txt
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-x86-64.tar.gz -o /work/jazzer.tar.gz \
    && echo '816b29fe8796e12ac0c8194dc47d4c245a21df6b00376e7ab42120ec985e3a42  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY build-native.sh /work/
RUN chmod +x /work/build-native.sh && /work/build-native.sh
COPY PdalPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; \
         clang --version | head -1; llvm-cov --version | sed -n 2p; } > /work/toolchain.txt

FROM --platform=linux/amd64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
# Runtime libraries of the source-built libpdalcpp (GDAL, GeoTIFF, PROJ, compression, XML, curl).
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libcurl4t64 libgdal34t64 libgeotiff5 liblzma5 libproj25 libxml2 libzstd1 zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/jni /work/jni
COPY --from=build /work/native /work/native
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/source/io/PlyReader.cpp /work/source/io/PlyReader.hpp /work/source/io/
COPY --from=build /work/source/LICENSE.txt /work/source/LICENSE.txt
COPY --from=build /work/abi-check.json /work/toolchain.txt /work/
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/native
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pdal-%p-%m.profraw
ENTRYPOINT ["/work/run-control.sh"]
