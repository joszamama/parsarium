FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 python3-venv python3-setuptools python3-wheel zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# pyassimp is a ctypes wrapper; it loads the Assimp shared library below. The same
# pinned Assimp 6.0.6 source as the C/C++ Assimp paths is built with only the PLY
# importer and LLVM source-region coverage, so AFL++ feedback comes from the
# native PLY parser rather than from the Python wrapper alone. The export API stays
# compiled (no exporters) because pyassimp binds aiExportScene when it loads.
RUN curl --fail --location --retry 3 \
    https://github.com/assimp/assimp/archive/refs/tags/v6.0.6.tar.gz \
    --output /work/assimp-6.0.6.tar.gz \
    && echo '5f7ed412b76575621df0525a762b31da5874afff352b3a890c6308db4ac7204c  /work/assimp-6.0.6.tar.gz' | sha256sum --check \
    && mkdir /work/assimp-source \
    && tar -xf /work/assimp-6.0.6.tar.gz -C /work/assimp-source --strip-components=1 \
    && echo '3ac1ba4f16e5826aeb5db0a6abb1319ea5bd4c41c1e90b507846f3d625ad6709  /work/assimp-source/code/AssetLib/Ply/PlyLoader.cpp' | sha256sum --check
RUN cmake -S /work/assimp-source -B /work/assimp-build -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_C_FLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' \
      -DCMAKE_CXX_FLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' \
      -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
      -DCMAKE_INSTALL_PREFIX=/opt/assimp -DCMAKE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=ON -DCMAKE_DEBUG_POSTFIX= \
      -DASSIMP_BUILD_TESTS=OFF -DASSIMP_BUILD_ASSIMP_TOOLS=OFF -DASSIMP_BUILD_SAMPLES=OFF \
      -DASSIMP_BUILD_ALL_IMPORTERS_BY_DEFAULT=OFF -DASSIMP_BUILD_PLY_IMPORTER=ON \
      -DASSIMP_BUILD_ALL_EXPORTERS_BY_DEFAULT=OFF -DASSIMP_NO_EXPORT=OFF \
      -DASSIMP_WARNINGS_AS_ERRORS=OFF -DASSIMP_INSTALL_PDB=OFF \
    && cmake --build /work/assimp-build -j"$(nproc)" \
    && cmake --install /work/assimp-build \
    && ls -l /opt/assimp/lib && test -f /opt/assimp/lib/libassimp.so.6.0.6
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/5f/f5577fe7f48be4d2bdf7e3284285469da80b99e4a4c34d4c927466317053/pyassimp-5.2.5.tar.gz --output /work/wheels/pyassimp-5.2.5.tar.gz \
    && echo '107d93780e4300d70698c4291c54dd32ff78e8cf0dafd56ac1801cd0260c36f3  /work/wheels/pyassimp-5.2.5.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ef/55/6dc6d6bb953bdfc52519a0059592c52b6e3b8ad51cf8256dffceb55b0610/setuptools-84.2.1-py3-none-any.whl --output /work/wheels/setuptools-84.2.1-py3-none-any.whl \
    && echo 'ca140b45d5325a9478f880e351484f62fef15f336462e449ca0c03c873d589c2  /work/wheels/setuptools-84.2.1-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps /work/wheels/pyassimp-5.2.5.tar.gz
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; echo 'Assimp 6.0.6 (source build, PLY importer only, LLVM coverage)'; /opt/venv/bin/pip show pyassimp atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/opt/assimp/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-assimp-%p.profraw
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 zlib1g && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /opt/assimp /opt/assimp
COPY --from=build /work/assimp-source/code/AssetLib/Ply /work/assimp-source/code/AssetLib/Ply
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
