FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# PyYAML 6.0.3: the wheel's Python package must match the pinned sdist byte for byte.
RUN mkdir /work/wheels /work/sdist /work/wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/f9/16491d7ed2a919954993e48aa941b200f38040928474c9e85ea9e64222c3/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5  /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/05/8e/961c0007c59b8dd7729d542c61a4d537767a59645b82a0b521206e1e25c2/pyyaml-6.0.3.tar.gz --output /work/sdist.tar.gz \
    && echo 'd76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f  /work/sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sdist.tar.gz --strip-components=1 -C /work/sdist \
    && unzip -q /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl -d /work/wheel \
    && diff -r --exclude=_yaml.cpython-314-x86_64-linux-gnu.so /work/sdist/lib/yaml /work/wheel/yaml \
    && grep -Fx 'License: MIT' /work/wheel/pyyaml-6.0.3.dist-info/METADATA \
    && cd /work/sdist \
    && printf '%s\n' \
       '60433788b652690c17710460da5d91e0c753d3318fd85f5e1e42862a71f25906  lib/yaml/scanner.py' \
       '8a55a9e6fbe0a07146cef3990c8b45a068c3e83e369e1959ad9ca30306b4a09a  lib/yaml/parser.py' \
       'fcaa37d16afa783594794a5ab94193dcb720f503c19ce3d59539c8311189f453  lib/yaml/composer.py' \
       '90d8247da78b524c10618fd0e857f54f3d97570fe91b5c5513d024ef3faf88b0  lib/yaml/constructor.py' \
       'f4bf9561f9b89961f1503d558385fbae30d12bfed565de9bf76c33abb63620a6  lib/yaml/resolver.py' \
       'd1d9b38ab3a20c6e17a38d519ee412ecaf6b918df18c78956ac7c330d4ea08dc  lib/yaml/reader.py' \
       'b19dfcc333d6a75dfd73073901164507252f271b41d3b5f7d85510033a0547a7  lib/yaml/__init__.py' \
       '8d3928f9dc4490fd635707cb88eb26bd764102a7282954307d3e5167a577e8a4  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/wheel/yaml /opt/venv/lib/python3.14/site-packages/yaml \
    && /opt/venv/bin/python -c 'import yaml; assert yaml.__version__ == "6.0.3"; assert yaml.SafeLoader.__module__ == "yaml.loader"; print(yaml.load(b"ready: true", Loader=yaml.SafeLoader))' \
    && { python3 --version; /opt/venv/bin/pip show PyYAML atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum yaml/scanner.py yaml/parser.py yaml/composer.py yaml/constructor.py yaml/resolver.py yaml/reader.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py structure.py run-control.py expected.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
