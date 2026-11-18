FROM --platform=linux/amd64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    binutils ca-certificates clang cmake curl libclang-rt-18-dev llvm ninja-build python3 unzip zip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# scalismo-vtk_3 1.0-RC1 depends on scalismo_3 1.0-RC1 (closure below, as in the scalismo project)
# and on vtkjavanativesall 0.2-RC1; of its per-platform natives only the Linux impl jar is fetched.
RUN mkdir /work/lib && cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo_3/1.0-RC1/scalismo_3-1.0-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/scala3-library_3/3.3.0/scala3-library_3-3.3.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.13.10/scala-library-2.13.10.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scalactic/scalactic_3/3.2.16/scalactic_3-3.2.16.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scalanlp/breeze_3/2.1.0/breeze_3-2.1.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scalanlp/breeze-macros_3/2.1.0/breeze-macros_3-2.1.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/dev/ludovic/netlib/blas/3.0.1/blas-3.0.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/dev/ludovic/netlib/lapack/3.0.1/lapack-3.0.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/dev/ludovic/netlib/arpack/3.0.1/arpack-3.0.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/net/sourceforge/f2j/arpack_combined_all/0.1/arpack_combined_all-0.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/net/sf/opencsv/opencsv/2.3/opencsv-2.3.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/github/wendykierp/JTransforms/3.1/JTransforms-3.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/pl/edu/icm/JLargeArrays/1.5/JLargeArrays-1.5.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/apache/commons/commons-math3/3.2/commons-math3-3.2.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.5/slf4j-api-1.7.5.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/modules/scala-collection-compat_3/2.7.0/scala-collection-compat_3-2.7.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/spire_3/0.18.0/spire_3-0.18.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/spire-macros_3/0.18.0/spire-macros_3-0.18.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/spire-platform_3/0.18.0/spire-platform_3-0.18.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/spire-util_3/0.18.0/spire-util_3-0.18.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/algebra_3/2.8.0/algebra_3-2.8.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/typelevel/cats-kernel_3/2.8.0/cats-kernel_3-2.8.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scalanlp/breeze-natives_3/2.1.0/breeze-natives_3-2.1.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo-niftijiojar/0.1.0/scalismo-niftijiojar-0.1.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo-hdf5-json_3/0.1-RC1/scalismo-hdf5-json_3-0.1-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/upickle_3/2.0.0/upickle_3-2.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/ujson_3/2.0.0/ujson_3-2.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/upickle-core_3/2.0.0/upickle-core_3-2.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/geny_3/0.7.1/geny_3-0.7.1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/upack_3/2.0.0/upack_3-2.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/lihaoyi/upickle-implicits_3/2.0.0/upickle-implicits_3-2.0.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/io/jhdf/jhdf/0.6.10/jhdf-0.6.10.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/com/ning/compress-lzf/1.1.2/compress-lzf-1.1.2.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/lz4/lz4-java/1.8.0/lz4-java-1.8.0.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/scala-lang/modules/scala-parallel-collections_3/1.0.4/scala-parallel-collections_3-1.0.4.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/org/slf4j/slf4j-nop/2.0.7/slf4j-nop-2.0.7.jar \
    && printf '%s\n' \
       '44bef8753f4bd90a7a0acda7ad2c632c6368fcc5daaf643f3a547060ca3dcf5f  scalismo_3-1.0-RC1.jar' \
       '78add3aaa13701690b73fd90a13d1cae1da32565dedb379e65ade30a16973f6b  scala3-library_3-3.3.0.jar' \
       'e6ca607c3fce03e8fa38af3374ce1f8bb098e316e8bf6f6d27331360feddb1c1  scala-library-2.13.10.jar' \
       'd6071fe5f4e6f97b25c473c3787098fc3e7cdebf224eeb12f3a48ad1b5816885  scalactic_3-3.2.16.jar' \
       'b178a21b7a14e157724549177547cae67aa5141be55f03c1fe7e7b184ed912db  breeze_3-2.1.0.jar' \
       '437a529f935c23a31176db3f3c27e8ec536ba491f08fe51aec8a613c865a80ff  breeze-macros_3-2.1.0.jar' \
       'f438e0b3dd2aa38133a837478052d5412e6a4e234f2fea2ed86c2d0386e2ad42  blas-3.0.1.jar' \
       '5262acf3c9294fe4529ed5ab7e4a1c8c6a733519f31fa9503dc80728cd719387  lapack-3.0.1.jar' \
       '62c0a0bda1e8b69140019c93215ab4eaf9d35ad6aa993502eecbaebcef965853  arpack-3.0.1.jar' \
       '9964fb948ef213548a79b23dd480af9d72f1450824fa006bbfea211ac1ffa6dc  arpack_combined_all-0.1.jar' \
       'dc0ba5bff6140dc92339973026a0ecbddc2a3b01bdd46ed9d16becc2f6d78de6  opencsv-2.3.jar' \
       'd9dffa3e27793040dccb97b054d95267df46e669c396bf1ca4f3b085069bc2d5  JTransforms-3.1.jar' \
       '6dca5ab23e1fdb9190a257c04687a9ea19111c36b6ec9478bce6b2a128ca1aeb  JLargeArrays-1.5.jar' \
       '6268a9a0ea3e769fc493a21446664c0ef668e48c93d126791f6f3f757978fee2  commons-math3-3.2.jar' \
       'fe30825245d2336c859dc38d60c0fc5f3668dbf29cd586828d2b5667ec355b91  slf4j-api-1.7.5.jar' \
       '6c39b8042527e6693ce6c966526b72f1c22dee3cc4767eca76cfd4d0a7f53385  scala-collection-compat_3-2.7.0.jar' \
       '755e6bca07ff0ddde6b2cbb984fe1178389a44887d5aaf610a1402e9fcfe99ac  spire_3-0.18.0.jar' \
       '65f223a3ccba177f96c999f0287527b18557eb14f92b7bda88d162c5d0696db8  spire-macros_3-0.18.0.jar' \
       '8b1dd10891b95e0e2cf2e375972fe0ee0fd231c31b150e352a6940d2bec89652  spire-platform_3-0.18.0.jar' \
       'de87255aa776a57ac105561e24673bde83a3d9980048582ab763be4e682ca42d  spire-util_3-0.18.0.jar' \
       '0ceb78004499e94dad2d0477dd92ce28319bad6c1af1e7e36b299312b40f60b6  algebra_3-2.8.0.jar' \
       'ac91c20eb0845fbb0286bc7f63c5a9ad5fc1fb48870468b957156f333bdacb86  cats-kernel_3-2.8.0.jar' \
       'aec81e2344f2c0e69b897bb301f1021f4a8d83f580de425502f69b36b99156a3  breeze-natives_3-2.1.0.jar' \
       'b65df46f4376eb78fd5b39f25fa4062a7b727bbae9542344d7b95717a941ee83  scalismo-niftijiojar-0.1.0.jar' \
       '9421e2c6740b42bd53e7907cb40f496adbc2fc707074fcb67cb737bcbd2eadef  scalismo-hdf5-json_3-0.1-RC1.jar' \
       '029d02943f93dd21df191343411e697824f98193cbc7e64a99d826348f0b2af0  upickle_3-2.0.0.jar' \
       'fafc5953023c92d6e83885060024a15677b06cf8b0dbc3b14d0cf458a25218bb  ujson_3-2.0.0.jar' \
       '4221f190469a2997cc490b82497ec6e6ac4b88d0d193bb83154ad36c19e05049  upickle-core_3-2.0.0.jar' \
       'a71cd6fadaa2bf4435b3e2651249efd7f3c586f3f4f4e763ff1d5794447ef669  geny_3-0.7.1.jar' \
       'fda68eb3c7578408ac4f7518304f52839c675833a35b15156a0e7448d2a57afd  upack_3-2.0.0.jar' \
       '6e0456ebe98cf43b02e724d3163cdc9248dd924e0be3c8edba43cc7cb540a69f  upickle-implicits_3-2.0.0.jar' \
       'b405d71bebfd1a8f4f097de71a0576bccbb5915d04b6d45a996e76cd20eea461  jhdf-0.6.10.jar' \
       'd919d904486c037f8d193412da0c92e22a9fa24230b9d67a57855c5c31c7e94e  commons-lang3-3.12.0.jar' \
       'a9a76c85a3cef3a22d4c0e8647a1449b638885f2ceb4d8c9f66df3c677cc228e  compress-lzf-1.1.2.jar' \
       'd74a3334fb35195009b338a951f918203d6bbca3d1d359033dc33edd1cadc9ef  lz4-java-1.8.0.jar' \
       'c3bf0d4d057942a78389fa9675823db5e3179f1b503f2df212b74e784da57050  scala-parallel-collections_3-1.0.4.jar' \
       '5411a0d44e2725182271230b9fb4c2c4062c1b5fa7df2d83e00c0302733db173  slf4j-nop-2.0.7.jar' \
       | sha256sum --check
RUN cd /work/lib \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo-vtk_3/1.0-RC1/scalismo-vtk_3-1.0-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/vtkjavanatives/0.2-RC1/vtkjavanatives-0.2-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/vtkjavanativesvtkjar/0.2-RC1/vtkjavanativesvtkjar-0.2-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/vtkjavanativesjogljar/0.2-RC1/vtkjavanativesjogljar-0.2-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/vtkjavanativesgluegenjar/0.2-RC1/vtkjavanativesgluegenjar-0.2-RC1.jar \
    && curl --fail --location --retry 3 -O https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/vtkjavanativeslinuximpl/0.2-RC1/vtkjavanativeslinuximpl-0.2-RC1.jar \
    && printf '%s\n' \
       '144efa53c1500fc38b64172e840366edff1e9548dd1208ce7ca2018209973fbf  scalismo-vtk_3-1.0-RC1.jar' \
       '2636d0e0282c996610f8510db62fae10251ff4ce21b59bba2d2a1987ce39328b  vtkjavanatives-0.2-RC1.jar' \
       'ae1ab89d1b9f61f218715ab19057dd668b0a22c2b3a939871001b8674ebf1dce  vtkjavanativesvtkjar-0.2-RC1.jar' \
       '69a1139f2546d78cb5bc195bb3397a91071ea5481851229825f7b9c3b6583c64  vtkjavanativesjogljar-0.2-RC1.jar' \
       '1a196212a1dd07b708d5039805a040f00b2b3b975ad332009ac5fc8b4d2b418f  vtkjavanativesgluegenjar-0.2-RC1.jar' \
       '8d87b0bfb08886052eb491be73e560ca561e74d7d371c616c06d5beab26982f4  vtkjavanativeslinuximpl-0.2-RC1.jar' \
       | sha256sum --check
RUN curl --fail --location --retry 3 -o /work/scalismo-vtk_3-1.0-RC1.pom https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo-vtk_3/1.0-RC1/scalismo-vtk_3-1.0-RC1.pom \
    && echo '6114559b2f43b1be8d85c1bd3aaf9ff8d71615bf117948e352eb30f3a099dea2  /work/scalismo-vtk_3-1.0-RC1.pom' | sha256sum --check \
    && grep -q 'Apache-2.0' /work/scalismo-vtk_3-1.0-RC1.pom
# Coverage subjects: the scalismo-vtk Scala sources (JaCoCo) and VTK 9.1.0 IO/PLY (LLVM).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/ch/unibas/cs/gravis/scalismo-vtk_3/1.0-RC1/scalismo-vtk_3-1.0-RC1-sources.jar -o /work/parser-sources.jar \
    && echo '392a407074fc3f9be865737d1cb41cc33db93ee5afee95777dc3ca38c0182e81  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && test -f /work/parser-source/scalismo/vtk/io/MeshIO.scala \
    && curl --fail --location --retry 3 https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz -o /work/VTK-9.1.0.tar.gz \
    && echo '8fed42f4f8f1eb8083107b68eaa9ad71da07110161a3116ad807f43e5ca5ce96  /work/VTK-9.1.0.tar.gz' | sha256sum --check \
    && mkdir -p /work/vtk/source && tar -xzf /work/VTK-9.1.0.tar.gz -C /work/vtk/source --strip-components=1 \
    && rm /work/VTK-9.1.0.tar.gz && test -f /work/vtk/source/IO/PLY/vtkPLYReader.cxx
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-x86-64.tar.gz -o /work/jazzer.tar.gz \
    && echo '816b29fe8796e12ac0c8194dc47d4c245a21df6b00376e7ab42120ec985e3a42  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY build-vtk.sh /work/
RUN chmod +x /work/build-vtk.sh && /work/build-vtk.sh
COPY check-native.sh /work/
RUN chmod +x /work/check-native.sh && /work/check-native.sh
COPY ScalismoVtkPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; \
         clang --version | head -1; llvm-cov --version | sed -n 2p; } > /work/toolchain.txt

FROM --platform=linux/amd64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
# Shared libraries the stock VTK, JOGL and AWT natives load (all are loaded at initialize()).
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libgl1 libglu1-mesa libx11-6 libxext6 libxi6 libxrender1 libxtst6 libxt6t64 libxcursor1 libxrandr2 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar /work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar
COPY --from=build /work/native-cov /work/native-cov
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/vtk/source/IO/PLY /work/vtk/source/IO/PLY
COPY --from=build /work/vtk/source/Copyright.txt /work/vtk/source/Copyright.txt
COPY --from=build /work/abi-check.json /work/toolchain.txt /work/
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
# scalismo.vtk.initialize() copies every native library of the impl jar into
# $user.home/.scalismo/vtkjavanatives-<platform>-<version> unless an identical (MD5) copy is
# already there, then loads them. Both homes are filled here, so the read-only runtime only
# verifies and loads: /work/home-stock from the stock jar, /work/home-cov from the copy whose
# libvtkIOPLY-9.1.so is the coverage build.
RUN printf 'ply\nformat ascii 1.0\nelement vertex 3\nproperty float x\nproperty float y\nproperty float z\nelement face 1\nproperty list uchar int vertex_indices\nend_header\n0 0 0\n1 0 0\n0 1 0\n3 0 1 2\n' > /work/controls-triangle.ply \
    && java -Duser.home=/work/home-stock -Djava.awt.headless=true \
      -cp '/work/classes:/work/lib/*' GenericHarness /work/controls-triangle.ply \
    && LLVM_PROFILE_FILE=/dev/null java -Duser.home=/work/home-cov -Djava.awt.headless=true \
      -cp "/work/classes:$(ls /work/lib/*.jar | grep -v vtkjavanativeslinuximpl | tr '\n' ':')/work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar" \
      GenericHarness /work/controls-triangle.ply \
    && rm /work/controls-triangle.ply
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
