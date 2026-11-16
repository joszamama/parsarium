FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build python3 python3-dev python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/66/34/fd86bf3ca48d010f3a588fa997595c13162bc07563382f9a4d5ec8855dfb/openmesh-1.2.1.tar.gz --output /work/wheels/openmesh-1.2.1.tar.gz \
    && echo '6fd3fa41a68148e4a7523f562426aa9758bf65ccc6642abcf79c37bae9c6af3c  /work/wheels/openmesh-1.2.1.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && mkdir /work/source \
    && tar -xzf /work/wheels/openmesh-1.2.1.tar.gz --strip-components=1 -C /work/source \
    && cd /work/source \
    && CMAKE_POLICY_VERSION_MINIMUM=3.5 CMAKE_BUILD_PARALLEL_LEVEL=4 \
       CXX=clang++ CXXFLAGS='-O0 -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps .
RUN { python3 --version; /opt/venv/bin/pip show openmesh atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && /opt/venv/bin/pip show numpy | grep -E '^(Name|Version):' >> /work/toolchain.txt
RUN sed -i 's/pybind11_add_module(openmesh /pybind11_add_module(openmesh NO_EXTRAS /' /work/source/CMakeLists.txt \
    && cmake --build /work/source/build-setuptools/temp.linux-x86_64-cpython-314 --config Release --parallel 4 \
    && cp /work/source/build-setuptools/lib.linux-x86_64-cpython-314/openmesh*.so /opt/venv/lib/python3.14/site-packages/ \
    && echo 'pybind11 NO_EXTRAS: LLVM coverage mapping retained' >> /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py merge-native-coverage.py run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
