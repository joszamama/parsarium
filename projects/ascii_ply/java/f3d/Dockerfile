FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    binutils ca-certificates clang cmake curl libclang-rt-18-dev llvm make python3 unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/f3d-app/f3d/archive/refs/tags/v4.0.1.tar.gz \
    --output /work/f3d-4.0.1.tar.gz \
    && echo '336dd26581a0a9b0bf9e6e9c900e3f103cf6df58971cfd5bbaf6fa93cd285560  /work/f3d-4.0.1.tar.gz' | sha256sum --check \
    && mkdir -p /work/f3d/source \
    && tar -xf /work/f3d-4.0.1.tar.gz -C /work/f3d/source --strip-components=1 \
    && rm /work/f3d-4.0.1.tar.gz \
    && cd /work/f3d/source && printf '%s\n' \
    '42e90e43576bfcc8945239179c49141c387c407a3a3c3696789d9f061cc4afb4  LICENSE.md' \
    '0b630f52d8b65a600337dd9992e95f6c010b410d85ff68801afeb4574f8ed902  THIRD_PARTY_LICENSES.md' \
    '20296423eceb968c4ea2cf442dbd570e72fe62e5bfcead15356d885dc098ec70  plugins/native/CMakeLists.txt' \
    'ea1b47b6e15952331f1ad141fd8091212ce3488a1e71c16308e95f60710629b4  plugins/native/ply.inl' \
    'a69e753d9d73ee7dc7685aa98711548d5773c21d9db3f05cecc86d3bbe12715d  plugins/native/module/vtkF3DPLYReader.h' \
    '585efa49df946d45785deb5784d6ba0bd496c9ec003e9b3c4409bcfd7411f73f  plugins/native/module/vtkF3DPLYReader.cxx' \
    '7d1caf2b94af39166a1cfdfdb3abbb777ad4cdf94e7156cf076b1409f35bab38  cmake/readerBoilerPlate.h.in' \
    '9e952132fd63881e2e1f98e33faabc7fa0755fd108175484b7e57b4a98ab68c8  cmake/plugin.cxx.in' \
    '8f5bbbc7fbf63b39687a557ef673b58eb7971dbccea1238153fe3d6a942b7e87  CMakeLists.txt' \
    '23fd353727c3df764f706f5f803606c5b5ec3d17b6c244488930074e5bd4df70  java/CMakeLists.txt' \
    '6ac4ea30e31a8adb9903b22817070d96526a5b9beaaa562cf45318c98b9cd580  java/Engine.java' \
    'c3fcba59b1851fe771b2bf18218ba406124e4cb27ba66e456a07b176a9e05b62  java/Scene.java' \
    'f972d163c063b0f459f6293aa52da9038ef9fddb6707a1879384c1e3f9be3191  java/Types.java' \
    '8e2e7cf3cb4805786ab79c12503a80f8d4e2bf9919df05b4e325dbce6c7f7be3  java/F3DEngineBindings.cxx' \
    '50497244a3aec691a66029cf34642878fc613bf378fe6cc2198aedda70e414fd  java/F3DSceneBindings.cxx' \
    '9f653674913c75bced4b2026cd33fa675ee7b7f3fa8839ae41ac8c3a55596732  library/plugin/reader.h' \
    'b836302207b797354579f6b6880293d5154890a316395a5cf44540bab3ae6bed  library/public/engine.h' \
    'f70cbfc6ca5d80991f3355f52d7a297033cb6a5ec12299fa96a3ef1842e558a9  library/public/scene.h' \
    '9922b5f1074ba4134d6c9d9ecefaea7d37e61d87db5467030a2e8014b77704b3  library/public/types.h' \
    '1389f72f6f7fc1a7cf4ea6d7268a9f677c4c47363615b8b943a66b8b344fbb07  library/src/scene_impl.cxx' \
    | sha256sum --check
RUN curl --fail --location --retry 3 \
    https://www.vtk.org/files/release/9.7/VTK-9.7.2.tar.gz \
    --output /work/VTK-9.7.2.tar.gz \
    && echo 'fecef55df5caec6298ce190024060a90ce3bb515033c0f18968b9ab5c12bf796  /work/VTK-9.7.2.tar.gz' | sha256sum --check \
    && mkdir -p /work/vtk/source \
    && tar -xf /work/VTK-9.7.2.tar.gz -C /work/vtk/source --strip-components=1 \
    && rm /work/VTK-9.7.2.tar.gz \
    && cd /work/vtk/source && printf '%s\n' \
    '3d07d5aaf2c4fe9114a8910644eb3c1491306b52ebb8bd92e4bc452459c87bfe  IO/PLY/vtkPLYReader.h' \
    'b13d4703d291fd48ffb329024748bf009add5667a0383172593f8d1ae0fec0b4  IO/PLY/vtkPLYReader.cxx' \
    'a9524f2714bf669816f3e70295e95a963f684a1755ada461e12b8cd188db93d6  IO/PLY/vtkPLY.h' \
    '9a76a055c85797a1e52fb2ee78198265270f39a2d7092ac3f481adef5d28061b  IO/PLY/vtkPLY.cxx' \
    'f986802c1b8a0498fdf559c65877b760422468c1bf9ca8243ae959e97f7530c1  IO/PLY/Copyright.txt' \
    '11232448be82e0ea2c2c66219c2e36389f42249894070ee10c549ff182fc08b6  Copyright.txt' \
    | sha256sum --check
COPY build-native.sh /work/build-native.sh
RUN chmod +x /work/build-native.sh && /work/build-native.sh vtk
COPY CMakeLists.txt /work/CMakeLists.txt
RUN /work/build-native.sh f3d
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
# JaCoCo maps the binding classes (package app.f3d.F3D) to the pinned Java sources.
RUN mkdir -p /work/parser-source/app/f3d/F3D && cp /work/f3d/source/java/*.java /work/parser-source/app/f3d/F3D/
COPY F3DPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; \
         clang --version | head -1; llvm-cov --version | sed -n 2p; cmake --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 \
    && rm -rf /var/lib/apt/lists/*
ENV HOME=/tmp XDG_CACHE_HOME=/tmp
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/native /work/native
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/f3d/source/java /work/f3d/source/java
COPY --from=build /work/f3d/source/plugins/native /work/f3d/source/plugins/native
COPY --from=build /work/f3d/source/LICENSE.md /work/f3d/source/THIRD_PARTY_LICENSES.md /work/f3d/source/
COPY --from=build /work/f3d/build/f3d/plugins/native/plugin.cxx /work/f3d/build/f3d/plugins/native/reader_PLYReader.h /work/f3d/build/f3d/plugins/native/
COPY --from=build /work/vtk/source/IO/PLY /work/vtk/source/IO/PLY
COPY --from=build /work/vtk/source/Copyright.txt /work/vtk/source/Copyright.txt
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
# The JNI library loads from /work/native; its LLVM profile goes to the writable tmpfs.
ENV JAVA_TOOL_OPTIONS=-Djava.library.path=/work/native
ENV LLVM_PROFILE_FILE=/tmp/parsarium-f3d-%p-%m.profraw
ENTRYPOINT ["/work/run-control.sh"]
