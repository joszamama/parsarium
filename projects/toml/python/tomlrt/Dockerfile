FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# tomlrt 2.3.3: pure-Python py3-none-any wheel; its tomlrt/ package must match the sdist src/tomlrt byte for byte.
RUN mkdir /work/wheels /work/tomlrt-sdist /work/tomlrt-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cc/f7/e95278e99677fdc69ecfde788ee6fc8d7309ac5e9e8805d1af2fa8e0debe/tomlrt-2.3.3-py3-none-any.whl --output /work/wheels/tomlrt-2.3.3-py3-none-any.whl \
    && echo '40a4c27d11566f1746673dd1693fec4f31d7f2e45a22483ec93d9a3a8554f63e  /work/wheels/tomlrt-2.3.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/72/76/d79f58d95f40b0a2fe66a34b770f9dbbba808457627d03b21af3a98f3e67/tomlrt-2.3.3.tar.gz --output /work/tomlrt-sdist.tar.gz \
    && echo '36782cf6821cd1962f34a548c2023984e4a60e32f286c36d7dc1430b77ac59ba  /work/tomlrt-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/tomlrt-sdist.tar.gz --strip-components=1 -C /work/tomlrt-sdist \
    && unzip -q /work/wheels/tomlrt-2.3.3-py3-none-any.whl -d /work/tomlrt-wheel \
    && diff -r /work/tomlrt-sdist/src/tomlrt /work/tomlrt-wheel/tomlrt \
    && grep -Fx 'License-Expression: MIT' /work/tomlrt-wheel/tomlrt-2.3.3.dist-info/METADATA \
    && ! grep '^Requires-Dist:' /work/tomlrt-wheel/tomlrt-2.3.3.dist-info/METADATA | grep -v "python_version < '3.12'" \
    && cd /work/tomlrt-sdist \
    && printf '%s\n' \
       'f37616527d5b95b9c252014a618f3d0fc035efe7716f5e00943b5079a85c1141  src/tomlrt/_parser.py' \
       'da6dc8f0b16dfdf066e14b2e676477751beec47aaa42e82293a8644851657c3c  src/tomlrt/_scanner.py' \
       '04b78e1cd291404933411696f5d814c25d241d47429c778cb6b87935fe3e3a6d  src/tomlrt/_scalar.py' \
       'ee1ed5fd980250f06582b6bd41b89c06eaada2ba574ebd348cd5d82e1fc042db  src/tomlrt/_public.py' \
       '780461fb6e04d3752b1f3e38abc891572b1544a0921f557cdb2d209b40b556cb  src/tomlrt/__init__.py' \
       'e225a9a6f9cbe6ec24d3ce4fed908c0ea58c0f0a988a95d82525ad643b2d58de  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/tomlrt-wheel/tomlrt /opt/venv/lib/python3.14/site-packages/tomlrt \
    && /opt/venv/bin/python -c 'import importlib.metadata as md, tomlrt; assert md.version("tomlrt") == "2.3.3"; print(tomlrt.loads("ready = true\n"))' \
    && { python3 --version; /opt/venv/bin/pip show tomlrt atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum tomlrt/_parser.py tomlrt/_scanner.py tomlrt/_scalar.py tomlrt/_public.py tomlrt/__init__.py; } > /work/toolchain.txt

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
