FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e1/7f/9f1237feb894afa472ef834aa1fbfe4d6398f28dc7e86a1b418650204c36/av-19.0.2-cp312-abi3-manylinux_2_28_x86_64.whl --output /work/wheels/av-19.0.2-cp312-abi3-manylinux_2_28_x86_64.whl \
    && echo '9c1da7aad0fa6c13b4a5c1e7985be0d13f8526a96284573acaf3d55ead6d3fe8  /work/wheels/av-19.0.2-cp312-abi3-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show av atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
