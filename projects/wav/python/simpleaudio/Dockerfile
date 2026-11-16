FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl gcc libasound2-dev python3 python3-dev python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/94/1b/4dc29653733202b68c09d9c6ca085cf67ac54859ee860647ef21ac1ff3dc/simpleaudio-1.0.4.tar.gz --output /work/wheels/simpleaudio-1.0.4.tar.gz \
    && echo '691c88649243544db717e7edf6a9831df112104e1aefb5f6038a5d071e8cf41d  /work/wheels/simpleaudio-1.0.4.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps /work/wheels/simpleaudio-1.0.4.tar.gz
RUN { python3 --version; /opt/venv/bin/pip show simpleaudio atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libasound2t64 libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
