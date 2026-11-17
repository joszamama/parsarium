FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dnspython 2.9.2: pure-Python py3-none-any wheel; its dns/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/dnspython-sdist /work/dnspython-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1e/0c/5346358b3a20275d256978c35203ddc2c8617f78c1b23795b79ba22ced6d/dnspython-2.9.2-py3-none-any.whl --output /work/wheels/dnspython-2.9.2-py3-none-any.whl \
    && echo 'af15f7d385a6ae2fb35a796fde2138004c8c42c7389090e2addc83e3b3340fd8  /work/wheels/dnspython-2.9.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/76/49/900383b471c645a3c397f47b3211d1fcecb3a540c98f683494cdf86b33de/dnspython-2.9.2.tar.gz --output /work/dnspython-sdist.tar.gz \
    && echo '8d4d39a513e649d634004ce4d39ade2352efcea472a0247535a5c2d18a9d7ba9  /work/dnspython-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/dnspython-sdist.tar.gz --strip-components=1 -C /work/dnspython-sdist \
    && unzip -q /work/wheels/dnspython-2.9.2-py3-none-any.whl -d /work/dnspython-wheel \
    && diff -r /work/dnspython-sdist/dns /work/dnspython-wheel/dns \
    && grep -Fx 'License-Expression: ISC' /work/dnspython-wheel/dnspython-2.9.2.dist-info/METADATA \
    && ! grep '^Requires-Dist:' /work/dnspython-wheel/dnspython-2.9.2.dist-info/METADATA | grep -v 'extra ==' \
    && cd /work/dnspython-wheel \
    && printf '%s\n' \
       '2874a85eba4292351b5abf6f8925d464f38584b8b07a9df38d40ea6b4c79feed  dns/message.py' \
       'b2c688d16963cf21e7579d58a165d99a235e9abf0c1a6706e7bbf20d45035512  dns/name.py' \
       '14801baaaf287eb22e7dcc3a9fd3b30e50a679f53e67a7bb382644f96c2ef643  dns/wire.py' \
       'c3ea3ff5654b329c19d3bc5f7481af623c3dded4a6145585499f843ad3d741cd  dnspython-2.9.2.dist-info/licenses/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/dnspython-wheel/dns /opt/venv/lib/python3.14/site-packages/dns \
    && /opt/venv/bin/python -c 'import dns.version; assert dns.version.version == "2.9.2"' \
    && { python3 --version; /opt/venv/bin/pip show dnspython atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum dns/message.py dns/name.py dns/wire.py; } > /work/toolchain.txt

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
