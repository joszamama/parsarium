FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dpkt 1.9.8: pure-Python py3-none-any wheel; its dpkt/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/dpkt-sdist /work/dpkt-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/11/79/479e2194c9096b92aecdf33634ae948d2be306c6011673e98ee1917f32c2/dpkt-1.9.8-py3-none-any.whl --output /work/wheels/dpkt-1.9.8-py3-none-any.whl \
    && echo '4da4d111d7bf67575b571f5c678c71bddd2d8a01a3d57d489faf0a92c748fbfd  /work/wheels/dpkt-1.9.8-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c9/7d/52f17a794db52a66e46ebb0c7549bf2f035ed61d5a920ba4aaa127dd038e/dpkt-1.9.8.tar.gz --output /work/dpkt-sdist.tar.gz \
    && echo '43f8686e455da5052835fd1eda2689d51de3670aac9799b1b00cfd203927ee45  /work/dpkt-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/dpkt-sdist.tar.gz --strip-components=1 -C /work/dpkt-sdist \
    && unzip -q /work/wheels/dpkt-1.9.8-py3-none-any.whl -d /work/dpkt-wheel \
    && diff -r /work/dpkt-sdist/dpkt /work/dpkt-wheel/dpkt \
    && grep -Fx 'License: BSD' /work/dpkt-wheel/dpkt-1.9.8.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/dpkt-wheel/dpkt-1.9.8.dist-info/METADATA \
    && cd /work/dpkt-wheel \
    && printf '%s\n' \
       'a85064c1eb8f65faca9e818388c53dd0be15d77c8d259482bfdb631cb4cf1cb4  dpkt/dns.py' \
       '78ec135f9f8cb5ddc5f564877bf8a0d35e1a3ba2ad54bb1a8a516d95c2493303  dpkt/dpkt.py' \
       '4c5ffde575425591cbd51410219a6b98bbbb717e0c5784187e356653da8e5095  dpkt-1.9.8.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/dpkt-wheel/dpkt /opt/venv/lib/python3.14/site-packages/dpkt \
    && /opt/venv/bin/python -c 'import dpkt; assert dpkt.__version__ == "1.9.8"' \
    && { python3 --version; /opt/venv/bin/pip show dpkt atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum dpkt/dns.py dpkt/dpkt.py; } > /work/toolchain.txt

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
