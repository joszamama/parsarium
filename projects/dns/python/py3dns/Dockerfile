FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# py3dns 4.0.2: pure-Python py3-none-any wheel; its DNS/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/py3dns-sdist /work/py3dns-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b7/43/1ff28f5302a0f423d4210cacc1f12fb416b6ba1f4c7107e020d264acb625/py3dns-4.0.2-py3-none-any.whl --output /work/wheels/py3dns-4.0.2-py3-none-any.whl \
    && echo '36bffe62b59a72cfa09c03f0bd3473e0126f20ee4285d14c07415dbf6f5fd571  /work/wheels/py3dns-4.0.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/76/67/d7e745a5248bd7ecf2b76d3a1c8280255cbbdcb21174b171cf3c87740836/py3dns-4.0.2.tar.gz --output /work/py3dns-sdist.tar.gz \
    && echo '98652e80ecec143c60f78f0e6b341631ca9a7560edd8dddfc864c02902618a39  /work/py3dns-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/py3dns-sdist.tar.gz --strip-components=1 -C /work/py3dns-sdist \
    && unzip -q /work/wheels/py3dns-4.0.2-py3-none-any.whl -d /work/py3dns-wheel \
    && diff -r /work/py3dns-sdist/DNS /work/py3dns-wheel/DNS \
    && grep -Fx 'Classifier: License :: OSI Approved :: Python License (CNRI Python License)' /work/py3dns-wheel/py3dns-4.0.2.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/py3dns-wheel/py3dns-4.0.2.dist-info/METADATA \
    && cd /work/py3dns-wheel \
    && printf '%s\n' \
       'd7ccd961e0bcb42662183f8d403bd906d3a5f0d8c6ea3986252b0f9a04f8ddb0  DNS/Lib.py' \
       'e68a32a4734451a20cd0324b941b67d0c6d7e3b9808e033f2d5829e7ea4c3c74  DNS/Base.py' \
       'ad70b1344da3ab6fe461fec7a53ae82273f59ad257744776b4f366b38a1c28ed  DNS/__init__.py' \
       'd1f23c3e3639c06eb57b30ddfbbf9fbb6f3324779f29846d4a10c98617dc968e  py3dns-4.0.2.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/py3dns-wheel/DNS /opt/venv/lib/python3.14/site-packages/DNS \
    && /opt/venv/bin/python -c 'import DNS; assert DNS.__version__ == "4.0.2"' \
    && { python3 --version; /opt/venv/bin/pip show py3dns atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum DNS/Lib.py DNS/Base.py DNS/__init__.py; } > /work/toolchain.txt

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
