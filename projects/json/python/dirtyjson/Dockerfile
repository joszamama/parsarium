FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dirtyjson 1.0.8: pure-Python py3-none-any wheel; its dirtyjson/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/dirtyjson-sdist /work/dirtyjson-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/68/69/1bcf70f81de1b4a9f21b3a62ec0c83bdff991c88d6cc2267d02408457e88/dirtyjson-1.0.8-py3-none-any.whl --output /work/wheels/dirtyjson-1.0.8-py3-none-any.whl \
    && echo '125e27248435a58acace26d5c2c4c11a1c0de0a9c5124c5a94ba78e517d74f53  /work/wheels/dirtyjson-1.0.8-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/db/04/d24f6e645ad82ba0ef092fa17d9ef7a21953781663648a01c9371d9e8e98/dirtyjson-1.0.8.tar.gz --output /work/dirtyjson-sdist.tar.gz \
    && echo '90ca4a18f3ff30ce849d100dcf4a003953c79d3a2348ef056f1d9c22231a25fd  /work/dirtyjson-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/dirtyjson-sdist.tar.gz --strip-components=1 -C /work/dirtyjson-sdist \
    && unzip -q /work/wheels/dirtyjson-1.0.8-py3-none-any.whl -d /work/dirtyjson-wheel \
    && diff -r /work/dirtyjson-sdist/dirtyjson /work/dirtyjson-wheel/dirtyjson \
    && grep -Fx 'License: MIT License' /work/dirtyjson-wheel/dirtyjson-1.0.8.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/dirtyjson-wheel/dirtyjson-1.0.8.dist-info/METADATA \
    && cd /work/dirtyjson-sdist \
    && printf '%s\n' \
       '13311a2c8dbf88356a005b18724fdef306a2ecdf114df5a7eeeca842a2b2cfa4  dirtyjson/loader.py' \
       '930e6c66fd1094285619a290f78d096be5aa300705bedc39f197f78e4e1c10d0  dirtyjson/__init__.py' \
       '83ada238112f94b08e06bd46164d914d4171403f548485b1fd4c8721945e45d4  dirtyjson/attributed_containers.py' \
       'e7bafeb422dd47aee32f00cbb65882eff2db1ed7ce93a274fc7014dc50794c4b  LICENSE.txt' \
       'fcaa1e313a99304322e2e0836ea4ee7d839ce9a480438f3922a853edfdde129f  simplejson.LICENSE.txt' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/dirtyjson-wheel/dirtyjson /opt/venv/lib/python3.14/site-packages/dirtyjson \
    && /opt/venv/bin/python -c 'import dirtyjson; print(dict(dirtyjson.loads(b"{\"ready\":true}")))' \
    && { python3 --version; /opt/venv/bin/pip show dirtyjson atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum dirtyjson/loader.py dirtyjson/__init__.py dirtyjson/attributed_containers.py; } > /work/toolchain.txt

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
