FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl libcairo2=1.18.4-3 libcairo2-dev=1.18.4-3 \
    libpng16-16t64=1.6.57-1ubuntu0.1 meson pkgconf python3 python3-dev \
    python3-mesonpy python3-venv \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update -qq && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bb/5e/19ab2572981a996ce96b853a189d2dcced40506b67d9555a7568457abcf2/pycairo-1.29.2.tar.gz --output /work/wheels/pycairo-1.29.2.tar.gz \
    && echo '3e69fff74fe64f5ba2dfa31f67c6bdf26413342574047437d2ac520d35e9a489  /work/wheels/pycairo-1.29.2.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && mkdir /work/source \
    && tar -xzf /work/wheels/pycairo-1.29.2.tar.gz --strip-components=1 -C /work/source \
    && cd /work/source \
    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps . \
    && cp -L /usr/lib/x86_64-linux-gnu/libpng16.so.16 /opt/venv/lib/libpng16.so.16
RUN { python3 --version; /opt/venv/bin/pip show pycairo atheris | grep -E '^(Name|Version):'; dpkg-query -W -f='${Package} ${Version}\n' libcairo2 libpng16-16t64; sha256sum /opt/venv/lib/libpng16.so.16; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libcairo2=1.18.4-3 libglib2.0-0 libpng16-16t64=1.6.57-1ubuntu0.1 python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
