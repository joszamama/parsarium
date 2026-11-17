FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# tomlkit 0.15.2: pure-Python py3-none-any wheel; its tomlkit/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/tomlkit-sdist /work/tomlkit-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/da/46/7d84138a60a8bd796825b2d38ebe92d0d16501ca57d501b7c5d677401bbc/tomlkit-0.15.2-py3-none-any.whl --output /work/wheels/tomlkit-0.15.2-py3-none-any.whl \
    && echo '05562412163a3037b94497385fb7f9204c637bc605af7a48199e41cf2272f437  /work/wheels/tomlkit-0.15.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/08/72/fc01563df95c189a9f65850096bdc205bc2fe37da6c740cd64afaf18d07e/tomlkit-0.15.2.tar.gz --output /work/tomlkit-sdist.tar.gz \
    && echo '83e32755ba1d20d9340bd069ee97e9f6232ba2346b63ffcba425de01f7e327a6  /work/tomlkit-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/tomlkit-sdist.tar.gz --strip-components=1 -C /work/tomlkit-sdist \
    && unzip -q /work/wheels/tomlkit-0.15.2-py3-none-any.whl -d /work/tomlkit-wheel \
    && diff -r /work/tomlkit-sdist/tomlkit /work/tomlkit-wheel/tomlkit \
    && grep -Fx 'License-Expression: MIT' /work/tomlkit-wheel/tomlkit-0.15.2.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/tomlkit-wheel/tomlkit-0.15.2.dist-info/METADATA \
    && cd /work/tomlkit-sdist \
    && printf '%s\n' \
       'a74abeff54ea1222a5bc113c29a2e824a4cc4778ebabdad36b9e91d004c8b92f  tomlkit/parser.py' \
       '2be326699043ae118d762fc4293ccdbf9e49d88f529af367cc9caf5bef45cefb  tomlkit/source.py' \
       '434e1d1cf2ccee906015062e216c268820dea5734c8153e7980dde3cb170a409  tomlkit/items.py' \
       '8d4315ba9d10e7fbc5b5460d124cf27cb73ff66a31b4b4dfdb8a66cebe93fcb6  tomlkit/container.py' \
       '5c6cb9ffb73b6ad19ccbe9fc498be363a9a5ec327582e516768b00ee358d36e3  tomlkit/api.py' \
       'f2f9b460ba719da6626add264d3782f275a4ff7aab677beda08b330911e23adb  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/tomlkit-wheel/tomlkit /opt/venv/lib/python3.14/site-packages/tomlkit \
    && /opt/venv/bin/python -c 'import tomlkit; assert tomlkit.__version__ == "0.15.2"; print(tomlkit.parse("ready = true\n").unwrap())' \
    && { python3 --version; /opt/venv/bin/pip show tomlkit atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum tomlkit/parser.py tomlkit/source.py tomlkit/items.py tomlkit/container.py; } > /work/toolchain.txt

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
