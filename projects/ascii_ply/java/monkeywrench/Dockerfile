FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/stephengold/MonkeyWrench/1.0.1/MonkeyWrench-1.0.1.jar -o /work/lib/MonkeyWrench-1.0.1.jar \
    && echo '84117be08e3f66317f7e00e420acfb6f4f3d37830af8812ef03f36ec19409423  /work/lib/MonkeyWrench-1.0.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6.jar -o /work/lib/lwjgl-assimp-3.3.6.jar \
    && echo '2cd29a9422bbc1bec11d49a18c7b289828eea939b66da2573d203a5a69ee8172  /work/lib/lwjgl-assimp-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6.jar -o /work/lib/lwjgl-3.3.6.jar \
    && echo 'b00e2781b74cc829db9d39fb68746b25bb7b94ce61d46293457dbccddabd999c  /work/lib/lwjgl-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/stephengold/Heart/9.3.0/Heart-9.3.0.jar -o /work/lib/Heart-9.3.0.jar \
    && echo '2765dda58ae9a8554080d6169ce376d39d46d009d0384932360d8e832e51825d  /work/lib/Heart-9.3.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jmonkeyengine/jme3-core/3.9.0-stable/jme3-core-3.9.0-stable.jar -o /work/lib/jme3-core-3.9.0-stable.jar \
    && echo '204822b39e121343f3c5f913a3b920d894cfd03c92a35fb33df770afad2f4b87  /work/lib/jme3-core-3.9.0-stable.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/stephengold/Wes/0.8.3/Wes-0.8.3.jar -o /work/lib/Wes-0.8.3.jar \
    && echo '99fc0712afe7d5e3f692861b5df7ca94f35e8282ef310f12cfc771f248094bb6  /work/lib/Wes-0.8.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jmonkeyengine/jme3-desktop/3.9.0-stable/jme3-desktop-3.9.0-stable.jar -o /work/lib/jme3-desktop-3.9.0-stable.jar \
    && echo '0f6f98115d252dc1b61e7aa5c4eb877da2435ea43846ed77fbaae6d8f96a72fb  /work/lib/jme3-desktop-3.9.0-stable.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jmonkeyengine/jme3-lwjgl3/3.9.0-stable/jme3-lwjgl3-3.9.0-stable.jar -o /work/lib/jme3-lwjgl3-3.9.0-stable.jar \
    && echo 'af92973504491081966728c57c1cd408c301bdc6692f238b8a6e03c64e30c02e  /work/lib/jme3-lwjgl3-3.9.0-stable.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjglx/lwjgl3-awt/0.2.3/lwjgl3-awt-0.2.3.jar -o /work/lib/lwjgl3-awt-0.2.3.jar \
    && echo 'abe1a021b282a01c4d00b53a07ffff946cfa85472ed1e11300a083c35f34572a  /work/lib/lwjgl3-awt-0.2.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-vulkan/3.3.5/lwjgl-vulkan-3.3.5-natives-macos-arm64.jar -o /work/lib/lwjgl-vulkan-3.3.5-natives-macos-arm64.jar \
    && echo 'a9360c956f11b9a5f98a5dc0c7b2f3b5f8809b0d05a762f6ba370cfa805a2823  /work/lib/lwjgl-vulkan-3.3.5-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6.jar -o /work/lib/lwjgl-glfw-3.3.6.jar \
    && echo 'b29c938ecc4997ce256a831aeca2033dab9829b5c21e72ebeb64aecd9e08450c  /work/lib/lwjgl-glfw-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jawt/3.3.6/lwjgl-jawt-3.3.6.jar -o /work/lib/lwjgl-jawt-3.3.6.jar \
    && echo '2093ee9a645689d43efd8c4f58ddd424f92a242813d93714642a3a2b45fdbf3e  /work/lib/lwjgl-jawt-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6.jar -o /work/lib/lwjgl-jemalloc-3.3.6.jar \
    && echo '194656f652d78b11c86e86757679e975acb94397a86f256c2225931c46d7ae71  /work/lib/lwjgl-jemalloc-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6.jar -o /work/lib/lwjgl-openal-3.3.6.jar \
    && echo '5d8669ee52325080f500cf0060785a13135a10c602286cefc8ba285805fa8468  /work/lib/lwjgl-openal-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opencl/3.3.6/lwjgl-opencl-3.3.6.jar -o /work/lib/lwjgl-opencl-3.3.6.jar \
    && echo 'e8eda96fe465e5e18124a1eb18ad8e10861e16056095bb9795827cfe0eb58444  /work/lib/lwjgl-opencl-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6.jar -o /work/lib/lwjgl-opengl-3.3.6.jar \
    && echo 'bb0430e0a5fd7b7b5770ae517960b2ea9887bb08d04f3a0cb1aae145332e1310  /work/lib/lwjgl-opengl-3.3.6.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-windows.jar -o /work/lib/lwjgl-3.3.6-natives-windows.jar \
    && echo 'a8d8edda34718bf70f68d14de1295b5bfc0f477a9607a3a9705d9e2d88538a8c  /work/lib/lwjgl-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-3.3.6-natives-windows-x86.jar \
    && echo '55ba30f2b07913ba59a8aefaa004b3c1e0aebe46655b91ef095f89ebc05bf37a  /work/lib/lwjgl-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-linux.jar -o /work/lib/lwjgl-3.3.6-natives-linux.jar \
    && echo '2f0e65d6985d602c0e5e5aab6576db113a9a378a36f8144ec93b77a4fde5876c  /work/lib/lwjgl-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-3.3.6-natives-linux-arm32.jar \
    && echo 'd54a952639f7a51714609415605e252e0c6be528601a11b60b5f9e9ff19f05de  /work/lib/lwjgl-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-3.3.6-natives-linux-arm64.jar \
    && echo '07643ee5e95635b710715b41900c2a05c3f08c74be9309ba0763e31431bfad3b  /work/lib/lwjgl-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-macos.jar -o /work/lib/lwjgl-3.3.6-natives-macos.jar \
    && echo 'a818cba530f8a541ef30e2cc2b731c8de2d081d25e9901959ff2bcdbf2344e0f  /work/lib/lwjgl-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl/3.3.6/lwjgl-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-3.3.6-natives-macos-arm64.jar \
    && echo 'e68652629a28f0262ca99a2132d370e3fbc70d9f10e11717afa3f2dbe85b64fc  /work/lib/lwjgl-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-windows.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-windows.jar \
    && echo '7492d3f62a868f857173d85360bb58716cd3fe8563da18419dde858aed2deb41  /work/lib/lwjgl-glfw-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-windows-x86.jar \
    && echo 'edb2470645c6a557b1604d8b22ff675f1ceecf653c85a3db4b531d309da1582d  /work/lib/lwjgl-glfw-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-linux.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-linux.jar \
    && echo 'a1b60014597bc0e45bf39089f4d838c3aa87fd668f6fe4e7326aa314d2ec87c0  /work/lib/lwjgl-glfw-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-linux-arm32.jar \
    && echo '75fd5d4225591ae6b0416e1b6fcefb2d85f1288bfabb15890bb4254e7be943e3  /work/lib/lwjgl-glfw-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-linux-arm64.jar \
    && echo '6a108ac764f88e0fc5b3c7de21227e7db123b1b27be531a93afb5954db4efa3f  /work/lib/lwjgl-glfw-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-macos.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-macos.jar \
    && echo '826f9da50850d3e7e3b2002897b672cbd999d6d8a174ceea1d6e874d148c4bc1  /work/lib/lwjgl-glfw-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-glfw/3.3.6/lwjgl-glfw-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-glfw-3.3.6-natives-macos-arm64.jar \
    && echo 'b46d40f15c2534e3800c5c44f73a4c7ded8a73b2272512c47847c1004ef7ffa9  /work/lib/lwjgl-glfw-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-windows.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-windows.jar \
    && echo '58371e1a9ef74ba94f559a18dc0c88f95e5e04c57f2b31850614e4e0a7a98c33  /work/lib/lwjgl-jemalloc-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-windows-x86.jar \
    && echo '91c715ae43af5c5a7cebeff5e4f708481723c8405fa4506bfb54966b3a91d61e  /work/lib/lwjgl-jemalloc-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-linux.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-linux.jar \
    && echo '5e5866a925abe5c0409f086ba114419202e408f7f8ad0a5a99b40b755c65b46c  /work/lib/lwjgl-jemalloc-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-linux-arm32.jar \
    && echo '11ec1ae93b7c7027e8feac902308ef40e65d7e3c4bf0aa91000b30f426d8990f  /work/lib/lwjgl-jemalloc-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-linux-arm64.jar \
    && echo '565fc2185052f9074b5e37bd31806d955e99e649351dfbe8c18bb8a372f0cfea  /work/lib/lwjgl-jemalloc-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-macos.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-macos.jar \
    && echo '81a78fb0ce8079da46e40e2c3ec98f32f54f2acb053f536a448a5bf594266445  /work/lib/lwjgl-jemalloc-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-jemalloc/3.3.6/lwjgl-jemalloc-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-jemalloc-3.3.6-natives-macos-arm64.jar \
    && echo 'ac8b95a42c37712049d0939249d913a19f6ebcab9d890809919e02f82194785d  /work/lib/lwjgl-jemalloc-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-windows.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-windows.jar \
    && echo 'b54a9d98686284947270e11e94c02aa15c30522119e7b80fcf0c98da6fa3c83c  /work/lib/lwjgl-opengl-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-windows-x86.jar \
    && echo '393f6d1a70fa673ca15b54b4e7ee7b0ca174eaf11613199df9f6dd502339b661  /work/lib/lwjgl-opengl-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-linux.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-linux.jar \
    && echo '8c0b5c081a7872a3cdb02b6448921da5ae5c23ab49656f299edc7a09b7e99b74  /work/lib/lwjgl-opengl-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-linux-arm32.jar \
    && echo 'abf7dbdf0f5a9110595b12a4ad0ae7ed6602e9a09bb234a6b8eba67ca2d82360  /work/lib/lwjgl-opengl-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-linux-arm64.jar \
    && echo '5bb6b9052f40df5d62fb43f06561b82307e4d50c48ab596ef73b9b2a59c446c1  /work/lib/lwjgl-opengl-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-macos.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-macos.jar \
    && echo '660fdc9f4f06083938b9e60ab7a3ce9bc9eb6d1c7e60cb54228796101b18b633  /work/lib/lwjgl-opengl-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-opengl/3.3.6/lwjgl-opengl-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-opengl-3.3.6-natives-macos-arm64.jar \
    && echo '2c0f67e7d36d71beed503043c06141af9fd83f5126a726eefceb7b5ba2aaf99c  /work/lib/lwjgl-opengl-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-windows.jar -o /work/lib/lwjgl-openal-3.3.6-natives-windows.jar \
    && echo '8ebb63e8014872709671161a896a720e2f09d038b0d3a33692218f7746504b35  /work/lib/lwjgl-openal-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-openal-3.3.6-natives-windows-x86.jar \
    && echo '3a3adad184f5ab9e165db721677c44f9f95f04bc4415a2dffc67640f8d00a863  /work/lib/lwjgl-openal-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-linux.jar -o /work/lib/lwjgl-openal-3.3.6-natives-linux.jar \
    && echo 'd30c407c1182f507c70ad12e21bac98189c767bf5c7a592dbfaa4f11d139545c  /work/lib/lwjgl-openal-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-openal-3.3.6-natives-linux-arm32.jar \
    && echo 'bd07f32fba66a04ae35e6834d3050a063058d0bbc5bd3c3197cd39b60cf871b2  /work/lib/lwjgl-openal-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-openal-3.3.6-natives-linux-arm64.jar \
    && echo '9cb8341ecd32b77a550f64afbb67f17464d1e61e252c44b3bbb521888176dca1  /work/lib/lwjgl-openal-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-macos.jar -o /work/lib/lwjgl-openal-3.3.6-natives-macos.jar \
    && echo 'e554a8c86f5b0c84d7136a8b1d050d6d76f228e7c1881e9f64de366f8b34258c  /work/lib/lwjgl-openal-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-openal/3.3.6/lwjgl-openal-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-openal-3.3.6-natives-macos-arm64.jar \
    && echo '99dbb6f65161cf6c966b5d064dd19285b6b0de202c8cd386bbb1115a5f84de22  /work/lib/lwjgl-openal-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-windows.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-windows.jar \
    && echo '55dff4359950fec9a26d49f3fbb755de861508cad293ed110575eeee496291f1  /work/lib/lwjgl-assimp-3.3.6-natives-windows.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-windows-x86.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-windows-x86.jar \
    && echo '4809ce36b970f83351eeec59c6aa8416f62142f68cf84111d079a4f9bbe68e2e  /work/lib/lwjgl-assimp-3.3.6-natives-windows-x86.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-linux.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-linux.jar \
    && echo '23a873bf7d6d1d7c87244c65951c5e4efb5122de7fbfd920f14723eff9fcddce  /work/lib/lwjgl-assimp-3.3.6-natives-linux.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-linux-arm32.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-linux-arm32.jar \
    && echo '4d79c94b31c5ed806ac40fb50194534e9de64c4f8e4828984fdc4fe7288da437  /work/lib/lwjgl-assimp-3.3.6-natives-linux-arm32.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-linux-arm64.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-linux-arm64.jar \
    && echo '609bcf9c23a6ad7e0841724af1fbdeaf02076cd1a69e61e01f4dda84171a4895  /work/lib/lwjgl-assimp-3.3.6-natives-linux-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-macos.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-macos.jar \
    && echo '997aef1f7ce242bb134e440f0aba24d8c5f2d7ab877b3ecef9402db0c0872822  /work/lib/lwjgl-assimp-3.3.6-natives-macos.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/lwjgl/lwjgl-assimp/3.3.6/lwjgl-assimp-3.3.6-natives-macos-arm64.jar -o /work/lib/lwjgl-assimp-3.3.6-natives-macos-arm64.jar \
    && echo '5782f015d41d0d29bf681c8ad6d46844ad3f6faa5d78c5e76351387ee2c0c010  /work/lib/lwjgl-assimp-3.3.6-natives-macos-arm64.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-tga/3.15.3/imageio-tga-3.15.3.jar -o /work/lib/imageio-tga-3.15.3.jar \
    && echo '87e3f8a0de1d4858fa89ae06886e18d1c97e2d0195a6466a17d135791bcf53a3  /work/lib/imageio-tga-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-core/3.15.3/imageio-core-3.15.3.jar -o /work/lib/imageio-core-3.15.3.jar \
    && echo '14d96b09384c48484b376127a0338f66875e94a67c99a3e94440a724bf1e0f09  /work/lib/imageio-core-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-lang/3.15.3/common-lang-3.15.3.jar -o /work/lib/common-lang-3.15.3.jar \
    && echo '24454ab8b23d8aaf54bb3a54e2187fdb5d96561905157852bdf75dddb730f426  /work/lib/common-lang-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-io/3.15.3/common-io-3.15.3.jar -o /work/lib/common-io-3.15.3.jar \
    && echo 'f5a164b4868ccef6baee5139d99b1b299fcc8f809dec882435b9a8fd61d473d3  /work/lib/common-io-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/common/common-image/3.15.3/common-image-3.15.3.jar -o /work/lib/common-image-3.15.3.jar \
    && echo '702f6edcbc91046c8a41c15d3a35e19aa3196536507169654370e3467e48c481  /work/lib/common-image-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-webp/3.15.3/imageio-webp-3.15.3.jar -o /work/lib/imageio-webp-3.15.3.jar \
    && echo '70d8fe5daddcdebfc3f548014bc8bb00dfee10d082c303e77c0fd5b177cf50b2  /work/lib/imageio-webp-3.15.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/twelvemonkeys/imageio/imageio-metadata/3.15.3/imageio-metadata-3.15.3.jar -o /work/lib/imageio-metadata-3.15.3.jar \
    && echo '24cdb4d24b3711026a220fc1c20557c82933662967803faada7c021d7caf6ff5  /work/lib/imageio-metadata-3.15.3.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/github/stephengold/MonkeyWrench/1.0.1/MonkeyWrench-1.0.1-sources.jar -o /work/parser-sources.jar \
    && echo '8032d8f4bc667402780ea9cd969f8eb67a1e8ee266f0a4360386d17de5071987  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source && unzip -q /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY MonkeyWrenchPlyAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
