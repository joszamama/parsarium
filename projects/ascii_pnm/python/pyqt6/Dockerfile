FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f9/cb/7557f6c559b392bb66a184eee802091676bf8e67a0d00f19a0dc10b5a7ae/pyqt6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyqt6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo '1922bf7440310845a4fd06f4242288084dc26cf682a67e561b115570a8def3d1  /work/wheels/pyqt6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d1/e5/c296a9bcde5ef9bbbc5249079422266ccd9c583d117c27d0e832861e9767/pyqt6_qt6-6.12.0-py3-none-manylinux_2_34_x86_64.whl --output /work/wheels/pyqt6_qt6-6.12.0-py3-none-manylinux_2_34_x86_64.whl \
    && echo 'b76e9962e83cf7daff9bb7ab169c804f37b77ab2d7393d3b380351f5a2441ee0  /work/wheels/pyqt6_qt6-6.12.0-py3-none-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bd/cc/6bee3cf016e053fa41579518614b835723ec33746ef8022e78302a9d905a/pyqt6_sip-13.13.1-cp314-cp314-manylinux1_x86_64.manylinux_2_5_x86_64.whl --output /work/wheels/pyqt6_sip-13.13.1-cp314-cp314-manylinux1_x86_64.manylinux_2_5_x86_64.whl \
    && echo 'c3bbc6d119c581d3f90a5c3cfc97025e6ae2ccc5bfc87a2fa68fe3d72ec2e631  /work/wheels/pyqt6_sip-13.13.1-cp314-cp314-manylinux1_x86_64.manylinux_2_5_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show PyQt6 atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 libdbus-1-3 libglib2.0-0 libgl1 libegl1 libxkbcommon0 libfreetype6 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
