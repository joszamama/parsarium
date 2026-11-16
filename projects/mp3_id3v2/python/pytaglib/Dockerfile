FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev libtag1-dev llvm python3 python3-dev python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/4e81cc7aae32c85eaaad614defe6fa9d4da82ea9dc452db9001036acfa64/pytaglib-3.2.0.tar.gz --output /work/wheels/pytaglib-3.2.0.tar.gz \
    && echo '964e32e86edcda107eb3821dd4ca226de04f7f0f99bb4c18737e138b4ed3313f  /work/wheels/pytaglib-3.2.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0c/51/ca221ec7e94b3c5dc4138dcdcbd41178df1729c1e88c5dfb25f9d30ba3da/cython-3.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/cython-3.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo '90f43be4eaa6afd58ce20d970bb1657a3627c44e1760630b82aa256ba74b4acb  /work/wheels/cython-3.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && mkdir /work/source \
    && tar -xzf /work/wheels/pytaglib-3.2.0.tar.gz --strip-components=1 -C /work/source \
    && cd /work/source \
    && CXX=clang++ CXXFLAGS='-O0 -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps .
RUN { python3 --version; /opt/venv/bin/pip show pytaglib atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libtag1-dev llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py merge-native-coverage.py run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
