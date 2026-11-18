FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# namespy 0.1.0: pure-Python py3-none-any wheel; its namespy/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/namespy-sdist /work/namespy-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e8/67/1b47fbc110e408636486ed1a73cc96694ffb5206c8483c71b2d3afa19152/namespy-0.1.0-py3-none-any.whl --output /work/wheels/namespy-0.1.0-py3-none-any.whl \
    && echo '9a3f20e38d60f38aa5536ef6704aa4c08e73c229bbc9637605f299ccb38d4fa2  /work/wheels/namespy-0.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/62/df/2a03546da898ba17268f5b7ee09702b7f1a551e5058a460ac8098d26bd79/namespy-0.1.0.tar.gz --output /work/namespy-sdist.tar.gz \
    && echo '535d1f60f0b62e780c9f809d1a7ff7d8b490914af0e2d52ad8f506e0c6b4b070  /work/namespy-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/namespy-sdist.tar.gz --strip-components=1 -C /work/namespy-sdist \
    && unzip -q /work/wheels/namespy-0.1.0-py3-none-any.whl -d /work/namespy-wheel \
    && diff -r /work/namespy-sdist/namespy /work/namespy-wheel/namespy \
    && grep -Fx 'License-Expression: Apache-2.0' /work/namespy-wheel/namespy-0.1.0.dist-info/METADATA \
    && ! grep '^Requires-Dist:' /work/namespy-wheel/namespy-0.1.0.dist-info/METADATA | grep -v 'extra ==' \
    && cd /work/namespy-wheel \
    && printf '%s\n' \
       '7542c7a90b63a9c1dae4debca71a972bc22b386467d339ea3406d171ad536660  namespy/packet.py' \
       '84f1de2e5c79428714ea9dd9dc4ca9e3e0f30d5204832f1fe6a313fff6a3bef1  namespy/wire.py' \
       '9625d099be05a91794e7989eaefd36c665a915506e190b16bf0294ce65111bd2  namespy/names.py' \
       'a681093b33f95ab5f82119fd73f8b9c101f8fc23ebdee1ca4a1c856f87f68cf8  namespy/rdata.py' \
       '2e29e7ec862f125b3644df43580765311c368f100a4e650d2950efce34647f04  namespy-0.1.0.dist-info/licenses/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/namespy-wheel/namespy /opt/venv/lib/python3.14/site-packages/namespy \
    && /opt/venv/bin/python -c 'import namespy, importlib.metadata as m; assert m.version("namespy") == "0.1.0"' \
    && { python3 --version; /opt/venv/bin/pip show namespy atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum namespy/packet.py namespy/wire.py namespy/names.py namespy/rdata.py; } > /work/toolchain.txt

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
