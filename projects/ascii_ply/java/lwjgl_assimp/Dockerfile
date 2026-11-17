FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    binutils ca-certificates clang cmake curl libclang-rt-18-dev llvm make python3 unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib /work/stock-jars \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.4.3/lwjgl-assimp-3.4.3.jar -o /work/lib/lwjgl-assimp-3.4.3.jar \
    && echo '6e42be582e5215a0d94a7fe098076426a988cc1c039287ba4eed8a73c4a78a5c  /work/lib/lwjgl-assimp-3.4.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.4.3/lwjgl-3.4.3.jar -o /work/lib/lwjgl-3.4.3.jar \
    && echo '46eeca5471833c3cf5da3c1da015b41e3bb3eb16dd3da03f366886da10096751  /work/lib/lwjgl-3.4.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.4.3/lwjgl-assimp-3.4.3-natives-linux-arm64.jar -o /work/stock-jars/lwjgl-assimp-3.4.3-natives-linux-arm64.jar \
    && echo '61abb8b377923b60a32c8a1102c1ee94828df6f478c0167c2602c572714b7dfa  /work/stock-jars/lwjgl-assimp-3.4.3-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.4.3/lwjgl-3.4.3-natives-linux-arm64.jar -o /work/stock-jars/lwjgl-3.4.3-natives-linux-arm64.jar \
    && echo '80a500dfb39fdea719a6bb2458235756e9b1e488fcbd7345aee9fd2cdaced6ff  /work/stock-jars/lwjgl-3.4.3-natives-linux-arm64.jar' | sha256sum --check
# Unmodified natives-linux-arm64 libraries. The jar names the Assimp revision it was built from.
RUN mkdir /work/stock-natives /work/native-stock \
    && unzip -q /work/stock-jars/lwjgl-assimp-3.4.3-natives-linux-arm64.jar -d /work/stock-natives \
    && unzip -q -o /work/stock-jars/lwjgl-3.4.3-natives-linux-arm64.jar -d /work/stock-natives \
    && test "$(cat /work/stock-natives/META-INF/linux/arm64/org/lwjgl/assimp/libassimp.so.git)" = 392a658f9c271be965271f45e7521a1b80ea4392 \
    && cp /work/stock-natives/linux/arm64/org/lwjgl/assimp/libassimp.so /work/stock-natives/linux/arm64/org/lwjgl/assimp/libdraco.so \
          /work/stock-natives/linux/arm64/org/lwjgl/liblwjgl.so /work/native-stock/ \
    && echo '481ea9e2e9ad866b8b0331eb356104a7ef9df10797af3a66294f94f2c6f6ace4  /work/native-stock/libassimp.so' | sha256sum --check \
    && echo '26f3ba4f6a073d8df33d8b083dfc9eeb80dae8f75627cabbefe355450b7614c2  /work/native-stock/libdraco.so' | sha256sum --check \
    && echo '8c9783382744d5a064f6b3df828f9af5ba83b03e58798b394c46611ca3dcd6d7  /work/native-stock/liblwjgl.so' | sha256sum --check
# Java wrapper sources (JaCoCo line mapping) and the Assimp source tree for that revision:
# LWJGL-CI/assimp 34f99dd = upstream 392a658 + LWJGL zlib update + LWJGL CI build configuration.
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.4.3/lwjgl-assimp-3.4.3-sources.jar -o /work/parser-sources.jar \
    && echo '178899579e85d3f89dc702ea36cf6f02d37c2c04b8708d39a2c5ed7876437f10  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source \
    && curl --fail --location --retry 3 https://codeload.github.com/LWJGL-CI/assimp/tar.gz/34f99dd81d93f2759d57c6c4dbfc85aa40a4b3d9 -o /work/assimp-34f99dd.tar.gz \
    && echo '1b662c12b96b34eea6def63ebbffe9a565d1c9a0e3ee5a87982fb5fae3fbb683  /work/assimp-34f99dd.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xf /work/assimp-34f99dd.tar.gz -C /work/source --strip-components=1 \
    && echo '042117da3e826eb67a8def782f6c04eb96b98c615f28eb91752d9bebf4b17760  /work/source/code/AssetLib/Ply/PlyLoader.cpp' | sha256sum --check \
    && echo '766dee1b136f633eb99799b045af2d3b6cc6783837c33eb0909a0e5db8326887  /work/source/code/AssetLib/Ply/PlyParser.cpp' | sha256sum --check \
    && echo '0e2c55e31299e56d604610d6ce937511dd58a05872b00d6ef09a31a36397ae1c  /work/source/include/assimp/scene.h' | sha256sum --check \
    && echo 'bedfc1177878b2f144145c1a12ac08735be620409581c01f4fe74939a93f8ecd  /work/source/include/assimp/mesh.h' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY LwjglAssimpPlyAdapter.java GenericHarness.java AbiLayout.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java
COPY abi_layout.c build-native.sh /work/
RUN chmod +x /work/build-native.sh && /work/build-native.sh \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; \
         clang --version | head -1; llvm-cov --version | sed -n 2p; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/native /work/native
COPY --from=build /work/native-stock /work/native-stock
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/source/code/AssetLib/Ply /work/source/code/AssetLib/Ply
COPY --from=build /work/abi-check.json /work/toolchain.txt /work/
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
# Profiles from the instrumented libraries go to the writable tmpfs outside run-control.sh.
ENV LLVM_PROFILE_FILE=/tmp/parsarium-assimp-%p-%m.profraw
ENTRYPOINT ["/work/run-control.sh"]
