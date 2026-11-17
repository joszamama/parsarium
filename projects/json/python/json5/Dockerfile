FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# json5 0.17.3: pure-Python py3-none-any wheel; its json5/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/json5-sdist /work/json5-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ae/39/e689b616c4279a821d5842a8a85c1874540f8d58e35028df93f2182120c2/json5-0.17.3-py3-none-any.whl --output /work/wheels/json5-0.17.3-py3-none-any.whl \
    && echo '2c8b22a893c35cd6a3c5ccbf1dd1c7d02c25dc1b5897fea658f9bf08c2e05f9a  /work/wheels/json5-0.17.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/1f/58a4d7ee466f81bc3c7337036380fc6d49de3afb7855d74f8121b1e89b32/json5-0.17.3.tar.gz --output /work/json5-sdist.tar.gz \
    && echo '8d0278ad34ebaa9c3af76d9519274811830224a2d1cd5af156dbd067f461b8a4  /work/json5-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/json5-sdist.tar.gz --strip-components=1 -C /work/json5-sdist \
    && unzip -q /work/wheels/json5-0.17.3-py3-none-any.whl -d /work/json5-wheel \
    && diff -r /work/json5-sdist/json5 /work/json5-wheel/json5 \
    && grep -Fx 'License-Expression: Apache-2.0' /work/json5-wheel/json5-0.17.3.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/json5-wheel/json5-0.17.3.dist-info/METADATA \
    && cd /work/json5-sdist \
    && printf '%s\n' \
       '41e539a013fad1a8c7278fa6eb62357acfb46cdff4987cc224af29e15993c7a7  json5/parser.py' \
       '416753da2dadf012cdb60ea2f4d9c81f21ab0ba0e0443025cc534e6b26685fb9  json5/lib.py' \
       'e2127cbdb467d31a1cbbc3d41b24c7fda12f92fae47dda1b565e7e0b2bc37c7c  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/json5-wheel/json5 /opt/venv/lib/python3.14/site-packages/json5 \
    && /opt/venv/bin/python -c 'import json5; assert json5.__version__ == "0.17.3"; print(json5.loads(b"{\"ready\":true}"))' \
    && { python3 --version; /opt/venv/bin/pip show json5 | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum json5/parser.py json5/lib.py; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py structure.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
