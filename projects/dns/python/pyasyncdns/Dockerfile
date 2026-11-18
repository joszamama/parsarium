FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# PyAsyncDNS 1.0.0 is published as a pure-Python sdist only (no dependencies); it is built offline with the
# pinned setuptools wheel and its installed package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/pyasyncdns-sdist /work/build-tools \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e2/ee/0a91d8599fb4192af7b7546f76acd56a7534213a9389b2c3ca741ba2b760/pyasyncdns-1.0.0.tar.gz --output /work/wheels/pyasyncdns-1.0.0.tar.gz \
    && echo '379e299887712e67a6f5b02d90b0be07d0c9bcb95ad3542a35a5830acaec079d  /work/wheels/pyasyncdns-1.0.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a3/dc/17031897dae0efacfea57dfd3a82fdd2a2aeb58e0ff71b77b87e44edc772/setuptools-80.9.0-py3-none-any.whl --output /work/build-tools/setuptools-80.9.0-py3-none-any.whl \
    && echo '062d34222ad13e0cc312a4c02d73f059e86a4acbfbdea8f8f76b28c99f306922  /work/build-tools/setuptools-80.9.0-py3-none-any.whl' | sha256sum --check \
    && tar -xzf /work/wheels/pyasyncdns-1.0.0.tar.gz --strip-components=1 -C /work/pyasyncdns-sdist \
    && grep -Fx 'Classifier: License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)' /work/pyasyncdns-sdist/PKG-INFO \
    && ! grep -q '^Requires-Dist:' /work/pyasyncdns-sdist/PKG-INFO \
    && cd /work/pyasyncdns-sdist \
    && printf '%s\n' \
       '0be32438c5ce03faa46c08bdb3562b6fdb0ea849284f2dd284ed8b3a55219cbf  PyAsyncDNS/codec.py' \
       '0587d7ca3e05bea0a391ef99c43664f805b8534b2370d44b2f1f5d1553f406ce  PyAsyncDNS/datatypes.py' \
       '1ff14ca02bd2fd648fd74a35b5d799e2e0853c281e067a9ba976fc49c4a3bac4  PyAsyncDNS/__init__.py' \
       '81cbae84a29ce7e770bf2bc7b178e50bda0ce8de6067aba661b0bc7b05b562f8  LICENSE.txt' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/build-tools/setuptools-80.9.0-py3-none-any.whl \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --no-build-isolation --require-hashes -r /work/runtime-requirements.lock \
    && /opt/venv/bin/pip uninstall --yes setuptools \
    && diff -r --exclude=__pycache__ /work/pyasyncdns-sdist/PyAsyncDNS /opt/venv/lib/python3.14/site-packages/PyAsyncDNS \
    && /opt/venv/bin/python -c 'import PyAsyncDNS, importlib.metadata as m; assert m.version("PyAsyncDNS") == "1.0.0"' \
    && { python3 --version; /opt/venv/bin/pip show PyAsyncDNS atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum PyAsyncDNS/codec.py PyAsyncDNS/datatypes.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
