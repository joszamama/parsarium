FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/72/20/5a6dcb0d28529ce6efe850755994c80817279eecf08620003775fda3b914/pyunpack-0.3-py2.py3-none-any.whl --output /work/wheels/pyunpack-0.3-py2.py3-none-any.whl \
    && echo '8f517cfc71215f37f74cf3a7668028828c68dc76f4d02e7a69f227ce978d51a3  /work/wheels/pyunpack-0.3-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9c/cf/27d1f4b3bae5e566f94fc716e048120128cf603d5163638d22bcd0fc92d8/EasyProcess-1.1-py3-none-any.whl --output /work/wheels/EasyProcess-1.1-py3-none-any.whl \
    && echo '82eed523a0a5eb12a81fa4eacd9f342caeb3f900eb4b798740e6696ad07e63f9  /work/wheels/EasyProcess-1.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/42/ee/84c8990b08efa0265bd10fc8781ef26e3157715bf0dfa47ee3c056b513d4/entrypoint2-1.1-py2.py3-none-any.whl --output /work/wheels/entrypoint2-1.1-py2.py3-none-any.whl \
    && echo 'eeb8c327bdb65cdd1668c023a6b110b7e3d1a046fb05e043861ebd9264b3a257  /work/wheels/entrypoint2-1.1-py2.py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show pyunpack atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
