FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/af/33/3136af92fbfe0354328d6b9674784c9a3b78371f34f34c3c4de318d03c73/pngtools-1.0.2-py3-none-any.whl --output /work/wheels/pngtools-1.0.2-py3-none-any.whl \
    && echo '906dd93160dcdc997545f22187b16e08cc54434063dbdbd01166b18f22b6d8e5  /work/wheels/pngtools-1.0.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl --output /work/wheels/attrs-26.1.0-py3-none-any.whl \
    && echo 'c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  /work/wheels/attrs-26.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/15/8b/15061b32332bb35ea2a2f6263d0f616779d576e82739ec8e7fcf3c94abf5/cmd2-1.5.0-py3-none-any.whl --output /work/wheels/cmd2-1.5.0-py3-none-any.whl \
    && echo '31aaeb590ec7bd2cc2cee0172099cc6f0a1396f82ab7bc389dbff23d9b90f6ec  /work/wheels/cmd2-1.5.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl --output /work/wheels/colorama-0.4.6-py2.py3-none-any.whl \
    && echo '4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6  /work/wheels/colorama-0.4.6-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/df/80/fc9d01d5ed37ba4c42ca2b55b4339ae6e200b456be3a1aaddf4a9fa99b8c/pyperclip-1.11.0-py3-none-any.whl --output /work/wheels/pyperclip-1.11.0-py3-none-any.whl \
    && echo '299403e9ff44581cb9ba2ffeed69c7aa96a008622ad0c46cb575ca75b5b84273  /work/wheels/pyperclip-1.11.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f7/5e/35c856e186b74678c24927847ad9895a51f1bc02a0c6126477a6c6040064/pyreadline3-3.5.6-py3-none-any.whl --output /work/wheels/pyreadline3-3.5.6-py3-none-any.whl \
    && echo '8449b734232e42a5dcd74048e39b60db2839a4c38cf3ae2bf7707d58b5389c0d  /work/wheels/pyreadline3-3.5.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6f/0c/309b1813b230d1dbbd6f2c2ab2bb21ef68992358977605d9ef289bbfedcc/wcwidth-0.9.4-py3-none-any.whl --output /work/wheels/wcwidth-0.9.4-py3-none-any.whl \
    && echo '901eace6d2dd25ebb917d0ce5db18e5c537e1504c905cf32f0d006c12098b05d  /work/wheels/wcwidth-0.9.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show pngtools atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
