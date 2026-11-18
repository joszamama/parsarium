FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# tomlclass 0.4.1: pure-Python py3-none-any wheel; its tomlclass/ package must match the sdist src/tomlclass byte for byte.
RUN mkdir /work/wheels /work/tomlclass-sdist /work/tomlclass-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/25/c7/210a82744d853ee86cbfc616e47915711bfc8ee8d9ed155c161c2dccc1da/tomlclass-0.4.1-py3-none-any.whl --output /work/wheels/tomlclass-0.4.1-py3-none-any.whl \
    && echo '924d6c00f161f3ea43a2d0a636ccae768da4d6965e90bdbf452130230431b587  /work/wheels/tomlclass-0.4.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7d/6a/3daffd200983c5fab6b615e32e74713fb53d9ce981b987bbe277f7a5b2c8/tomlclass-0.4.1.tar.gz --output /work/tomlclass-sdist.tar.gz \
    && echo '363f17d5982848a8a85080e8e90a812bcad9651da757b239a20a564beb72309b  /work/tomlclass-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/tomlclass-sdist.tar.gz --strip-components=1 -C /work/tomlclass-sdist \
    && unzip -q /work/wheels/tomlclass-0.4.1-py3-none-any.whl -d /work/tomlclass-wheel \
    && diff -r /work/tomlclass-sdist/src/tomlclass /work/tomlclass-wheel/tomlclass \
    && grep -Fx 'License-Expression: MIT' /work/tomlclass-wheel/tomlclass-0.4.1.dist-info/METADATA \
    && ! grep '^Requires-Dist:' /work/tomlclass-wheel/tomlclass-0.4.1.dist-info/METADATA | grep -v "extra == " \
    && cd /work/tomlclass-sdist \
    && printf '%s\n' \
       '11c577d8b88c04ec9f9b6bda245dfffda4063c8408bf8ac92ebe3d02f9af28e7  src/tomlclass/parser.py' \
       '5e7544d405d3e7caebdf2b2c08db4a6ae63bbf06fa72b57dae9a2a87d4f9a8b6  src/tomlclass/nodes.py' \
       '62964585107134b19e8e7d73c803a6dd460e390935b30bc54fc34116fffc16cb  src/tomlclass/_document.py' \
       '05ea45289ebdd59b51c77c92d86f1faf0ecba3e227904b25161dc854ad56e997  src/tomlclass/__init__.py' \
       '38eeea1cea3a41dbd96a1bdff0d4df9207151ae87c7ea15cc4a4efc666e6cff9  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/tomlclass-wheel/tomlclass /opt/venv/lib/python3.14/site-packages/tomlclass \
    && /opt/venv/bin/python -c 'import tomlclass; assert tomlclass.__version__ == "0.4.1"; print(tomlclass.loads("ready = true\n"))' \
    && { python3 --version; /opt/venv/bin/pip show tomlclass atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum tomlclass/parser.py tomlclass/nodes.py tomlclass/_document.py tomlclass/__init__.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY expected /work/expected
COPY harness.py fuzz.py replay.py structure.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
