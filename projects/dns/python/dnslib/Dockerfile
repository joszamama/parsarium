FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dnslib 0.9.26: pure-Python py3-none-any wheel; its dnslib/ package must match the sdist (minus the sdist-only dnslib/test) byte for byte.
RUN mkdir /work/wheels /work/dnslib-sdist /work/dnslib-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/93/167364f10194e374119b211e475ed8763d7591ae4f7001b304282dde5825/dnslib-0.9.26-py3-none-any.whl --output /work/wheels/dnslib-0.9.26-py3-none-any.whl \
    && echo 'e68719e633d761747c7e91bd241019ef5a2b61a63f56025939e144c841a70e0d  /work/wheels/dnslib-0.9.26-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a2/71/269f74ef9bc8ca453af2e1768d4f4c8e7ef5f894d058d27fd1b69c754d7f/dnslib-0.9.26.tar.gz --output /work/dnslib-sdist.tar.gz \
    && echo 'be56857534390b2fbd02935270019bacc5e6b411d156cb3921ac55a7fb51f1a8  /work/dnslib-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/dnslib-sdist.tar.gz --strip-components=1 -C /work/dnslib-sdist \
    && unzip -q /work/wheels/dnslib-0.9.26-py3-none-any.whl -d /work/dnslib-wheel \
    && diff -r --exclude=test /work/dnslib-sdist/dnslib /work/dnslib-wheel/dnslib \
    && grep -Fx 'License: BSD' /work/dnslib-wheel/dnslib-0.9.26.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/dnslib-wheel/dnslib-0.9.26.dist-info/METADATA \
    && cd /work/dnslib-wheel \
    && printf '%s\n' \
       '2fb898bba0415f8a551de0862fb16b244b3650bea640a04e2ce9c8e8b2142caa  dnslib/dns.py' \
       '77c57d8b170aeb7ae7625f3fce8c73b4daa20d5dcbc51bb9f25aa228ec92df6d  dnslib/buffer.py' \
       '0afd166fa8edf21482eed3defb841b63c98dd818dbd97b24b2dcf90cca46b876  dnslib/label.py' \
       'a4c62a28374d8211cd4c20c650f6923882ed5993d52297b47303d5aaeb17696f  dnslib-0.9.26.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/dnslib-wheel/dnslib /opt/venv/lib/python3.14/site-packages/dnslib \
    && /opt/venv/bin/python -c 'import dnslib; assert dnslib.version == "0.9.26"' \
    && { python3 --version; /opt/venv/bin/pip show dnslib atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum dnslib/dns.py dnslib/buffer.py dnslib/label.py; } > /work/toolchain.txt

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
