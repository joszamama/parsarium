FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/93/38/8e67f280c571d256fa168cac1dfeec190659cf415dfea0e0771667d22b54/pyntcloud-0.3.1-py2.py3-none-any.whl --output /work/wheels/pyntcloud-0.3.1-py2.py3-none-any.whl \
    && echo '2c064f53ae75175e8a9b8fe9f59d430b02b203a4e7ef8620af01d5e247d4df88  /work/wheels/pyntcloud-0.3.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/23/c3/dcf098d687f1f31c97b9c3869809fa2cdb6598039299167f6dfe0cf0c3a5/pandas-3.1.1-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pandas-3.1.1-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl \
    && echo '326459d8a9be11b5f48c7fc1d63e38ba7cfeaebe5d41bd19e4c5f4f11dc9ac91  /work/wheels/pandas-3.1.1-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2f/a9/52b89563d154433d79b51ed1eb4842bf7334cb2696891a7fe135618853d7/python_dateutil-4.0.0-py3-none-any.whl --output /work/wheels/python_dateutil-4.0.0-py3-none-any.whl \
    && echo 'a5e246f79eb80475e691bf93862cead98decd8a498cf53ba0516fcdc0f50dc1c  /work/wheels/python_dateutil-4.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6b/89/2a844506d49651e9aa1af6ef95b6bd8031cb1d5a4375edec6155037e04cf/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'ac0333bdf38309aa3dcbe7e3fa7ea29e7a2c37c6ea306a757b700ded8e4596ad  /work/wheels/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0a/66/9a06c2227fedfd4919f0eaaa8b94377d9730882a7e4f95823c9a331ab5e1/tzdata-2026.6-py2.py3-none-any.whl --output /work/wheels/tzdata-2026.6-py2.py3-none-any.whl \
    && echo '0a10eec6e13ef16b627fabed9a5f2ba61a62b1c67f327305f4e7e412a70b4aec  /work/wheels/tzdata-2026.6-py2.py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show pyntcloud atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
