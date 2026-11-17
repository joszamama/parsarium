FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# hjson 3.1.0: pure-Python py3-none-any wheel; its hjson/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/hjson-sdist /work/hjson-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1f/7f/13cd798d180af4bf4c0ceddeefba2b864a63c71645abc0308b768d67bb81/hjson-3.1.0-py3-none-any.whl --output /work/wheels/hjson-3.1.0-py3-none-any.whl \
    && echo '65713cdcf13214fb554eb8b4ef803419733f4f5e551047c9b711098ab7186b89  /work/wheels/hjson-3.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/82/e5/0b56d723a76ca67abadbf7fb71609fb0ea7e6926e94fcca6c65a85b36a0e/hjson-3.1.0.tar.gz --output /work/hjson-sdist.tar.gz \
    && echo '55af475a27cf83a7969c808399d7bccdec8fb836a07ddbd574587593b9cdcf75  /work/hjson-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/hjson-sdist.tar.gz --strip-components=1 -C /work/hjson-sdist \
    && unzip -q /work/wheels/hjson-3.1.0-py3-none-any.whl -d /work/hjson-wheel \
    && diff -r /work/hjson-sdist/hjson /work/hjson-wheel/hjson \
    && grep -Fx 'License: MIT License' /work/hjson-wheel/hjson-3.1.0.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/hjson-wheel/hjson-3.1.0.dist-info/METADATA \
    && cd /work/hjson-sdist \
    && printf '%s\n' \
       'a07cfb836b107784be0096d2ceeafd5495aa0070d62f6e45550f86df95e51820  hjson/decoder.py' \
       '20bf29a101af0ac6fcdb2eea6398eb952ad9e717043693d4b62ded34a869ad8c  hjson/scanner.py' \
       '3f2d5dac056df97a62db12401f15570dd5fe367882e259716553e363b3323c26  hjson/__init__.py' \
       '591c51f49c6833bce1a5d53e63785a0467add6745a5a880e4d10f4e64cc44c4c  LICENSE.txt' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/hjson-wheel/hjson /opt/venv/lib/python3.14/site-packages/hjson \
    && /opt/venv/bin/python -c 'import hjson; assert hjson.__version__ == "3.1.0"; print(dict(hjson.loads(b"{\"ready\":true}")))' \
    && { python3 --version; /opt/venv/bin/pip show hjson atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum hjson/decoder.py hjson/scanner.py hjson/__init__.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py structure.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
