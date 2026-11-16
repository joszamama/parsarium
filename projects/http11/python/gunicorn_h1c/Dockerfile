FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl llvm python3 python3-dev python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update -qq && apt-get install -y --no-install-recommends libclang-rt-21-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/57/47/134d251046d403462cca9089eeeef9473a9ce215607b00cac4c2451a8a9a/gunicorn_h1c-0.6.14.tar.gz --output /work/wheels/gunicorn_h1c-0.6.14.tar.gz \
    && echo 'afddb1f706bfe28c69fbf050107a5a157a34ea1d6af0ea1fbfd98ca2b5ca4eb0  /work/wheels/gunicorn_h1c-0.6.14.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && mkdir /work/source \
    && tar -xzf /work/wheels/gunicorn_h1c-0.6.14.tar.gz --strip-components=1 -C /work/source \
    && cd /work/source \
    && CC=clang CFLAGS='-O0 -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps .
RUN { python3 --version; /opt/venv/bin/pip show gunicorn-h1c atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

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
