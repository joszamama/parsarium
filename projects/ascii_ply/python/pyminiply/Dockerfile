FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build python3 python3-dev python3-packaging python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b1/46/cc352a40595c7c736ccb6b07e6d7a4db9b71087dcf5caef2343150d0d0db/pyminiply-0.2.3.tar.gz --output /work/wheels/pyminiply-0.2.3.tar.gz \
    && echo 'f024b81bd222a03840d6ff9f264a565cea30c7cb02cc197b83dab99e83ddbfe7  /work/wheels/pyminiply-0.2.3.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/43/49/ec16b3db6893db788ae35f98506ff5a9c25dca7eb18cc38ada8a4c1dc944/scikit_build_core-0.11.6-py3-none-any.whl --output /work/wheels/scikit_build_core-0.11.6-py3-none-any.whl \
    && echo 'ce6d8fe64e6b4c759ea0fb95d2f8a68f60d2df31c2989838633b8ec930736360  /work/wheels/scikit_build_core-0.11.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/3f/d81fa4c0d1450c6f58f5b5708082617949c12c5e98c1fae0d94a9e3a9b8f/nanobind-2.8.0-py3-none-any.whl --output /work/wheels/nanobind-2.8.0-py3-none-any.whl \
    && echo '80fd403cfe4c8553b237ba5fbb62971921e2c5d1e6eb4a2fd457c67f987ab56f  /work/wheels/nanobind-2.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cc/20/ff623b09d963f88bfde16306a54e12ee5ea43e9b597108672ff3a408aad6/pathspec-0.12.1-py3-none-any.whl --output /work/wheels/pathspec-0.12.1-py3-none-any.whl \
    && echo 'a0d503e138a4c123b27490a4f7beda6a01c6f288df0e4a8b79c7eb0dc7b4cc08  /work/wheels/pathspec-0.12.1-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && mkdir /work/source \
    && tar -xzf /work/wheels/pyminiply-0.2.3.tar.gz --strip-components=1 -C /work/source \
    && cd /work/source \
    && CXX=clang++ CXXFLAGS='-O0 -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps .
RUN { python3 --version; /opt/venv/bin/pip show pyminiply atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

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
