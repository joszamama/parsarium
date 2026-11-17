FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Twisted 26.10.0 (py3-none-any wheel) and its seven runtime requirements, all pinned by hash.
RUN mkdir /work/wheels /work/twisted-wheel && cd /work/wheels \
    && for url in \
       https://files.pythonhosted.org/packages/10/93/fdfa79229fdc19a6542086d46b5c5d424ee62a6408d25657e8690e0a745f/twisted-26.10.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/02/ff/1175b0b7371e46244032d43a56862d0af455823b5280a50c63d99cc50f18/automat-25.4.16-py3-none-any.whl \
       https://files.pythonhosted.org/packages/b8/40/c199d095151addf69efdb4b9ca3a4f20f70e20508d6222bffb9b76f58573/constantly-23.10.4-py3-none-any.whl \
       https://files.pythonhosted.org/packages/6e/aa/8caf6a0a3e62863cbb9dab27135660acba46903b703e224f14f447e57934/hyperlink-21.0.0-py2.py3-none-any.whl \
       https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl \
       https://files.pythonhosted.org/packages/1d/55/0f4df2a44053867ea9cbea73fc588b03c55605cd695cee0a3d86f0029cb2/incremental-24.11.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl \
       https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/50/03/372676f4a91df53b9fae808b26fac6fce3d8e02bfa0e134162d11a7b607b/zope_interface-8.7-cp314-cp314-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl \
       https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl; \
       do curl --fail --location --retry 3 -O "$url" || exit 1; done \
    && printf '%s\n' \
       '3732f42af218925a0fe78d6668db55853f7fb532245a89a2669babe7d3000fa8  twisted-26.10.0-py3-none-any.whl' \
       'c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  attrs-26.1.0-py3-none-any.whl' \
       '04e9bce696a8d5671ee698005af6e5a9fa15354140a87f4870744604dcdd3ba1  automat-25.4.16-py3-none-any.whl' \
       '3fd9b4d1c3dc1ec9757f3c52aef7e53ad9323dbe39f51dfd4c43853b68dfa3f9  constantly-23.10.4-py3-none-any.whl' \
       'e6b14c37ecb73e89c77d78cdb4c2cc8f3fb59a885c5b3f819ff4ed80f25af1b4  hyperlink-21.0.0-py2.py3-none-any.whl' \
       'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c  idna-3.20-py3-none-any.whl' \
       'a34450716b1c4341fe6676a0598e88a39e04189f4dce5dc96f656e040baa10b3  incremental-24.11.0-py3-none-any.whl' \
       'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  packaging-26.3-py3-none-any.whl' \
       '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  typing_extensions-4.16.0-py3-none-any.whl' \
       '6260ccc856a2c561b20341a74a8c1d9bb13916f6b52e880f336a0ddf61a1b726  zope_interface-8.7-cp314-cp314-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl' \
       '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       | sha256sum --check \
    && unzip -q /work/wheels/twisted-26.10.0-py3-none-any.whl -d /work/twisted-wheel \
    && grep -Fx 'License-Expression: MIT' /work/twisted-wheel/twisted-26.10.0.dist-info/METADATA \
    && cd /work/twisted-wheel \
    && printf '%s\n' \
       'a07bd438f7c03c9382a89e6402d8be2a07c02e4fe967a9c6349dcdd17b4c328a  twisted/names/dns.py' \
       'd7a2f74fe5c2b3f610052b75b5a131728c49823b28088893dacacf8d58849a4d  twisted-26.10.0.dist-info/licenses/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/twisted-wheel/twisted/names /opt/venv/lib/python3.14/site-packages/twisted/names \
    && /opt/venv/bin/python -c 'import twisted.names.dns, importlib.metadata as m; assert m.version("twisted") == "26.10.0"' \
    && { python3 --version; /opt/venv/bin/pip show twisted zope.interface atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum twisted/names/dns.py; } > /work/toolchain.txt

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
