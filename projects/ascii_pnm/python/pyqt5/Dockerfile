FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b4/8c/4065950f9d013c4b2e588fe33cf04e564c2322842d84dbcbce5ba1dc28b0/PyQt5-5.15.11-cp38-abi3-manylinux_2_17_x86_64.whl --output /work/wheels/PyQt5-5.15.11-cp38-abi3-manylinux_2_17_x86_64.whl \
    && echo 'cd672a6738d1ae33ef7d9efa8e6cb0a1525ecf53ec86da80a9e1b6ec38c8d0f1  /work/wheels/PyQt5-5.15.11-cp38-abi3-manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/de/a0/dd9889ed9bf100d6d8b9d608b2689dc2a7f871f9489a0c563a8cf78c329f/pyqt5_qt5-5.15.19-py3-none-manylinux2014_x86_64.whl --output /work/wheels/pyqt5_qt5-5.15.19-py3-none-manylinux2014_x86_64.whl \
    && echo '31421d9c31fb29a8faee4b8b3c32658fb51a9e8c4c708075121162fa44faf80e  /work/wheels/pyqt5_qt5-5.15.19-py3-none-manylinux2014_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/87/6e/caea55c1039d5189c43d03799a3fd781f9959d8e540363bdada64c1f82db/pyqt5_sip-12.20.1-cp314-cp314-manylinux_2_5_x86_64.manylinux1_x86_64.whl --output /work/wheels/pyqt5_sip-12.20.1-cp314-cp314-manylinux_2_5_x86_64.manylinux1_x86_64.whl \
    && echo 'd815b444fba57024a5f051905286c048792ded4edc89ea5de40a8c5f2f8fcd21  /work/wheels/pyqt5_sip-12.20.1-cp314-cp314-manylinux_2_5_x86_64.manylinux1_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show PyQt5 atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
