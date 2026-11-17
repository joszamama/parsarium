FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# yamlcore 0.1.1: the wheel's Python package must match the pinned sdist byte for byte.
# PyYAML 6.0.3 is the same pinned wheel as projects/yaml/python/pyyaml.
RUN mkdir /work/wheels /work/sdist /work/wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d6/80/17597c65886db896fcd3d9d272156f269b42792ed6ba29b2b327c9b6265a/yamlcore-0.1.1-py3-none-any.whl --output /work/wheels/yamlcore-0.1.1-py3-none-any.whl \
    && echo '85adda6abfe2ed6b13c80818d6b733f286bd6685314f7e6705321f4477f2dba1  /work/wheels/yamlcore-0.1.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/f9/16491d7ed2a919954993e48aa941b200f38040928474c9e85ea9e64222c3/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5  /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f2/ff/d96b723fe194349df8547f26324146bd3f60e7c0c5ccbc39717ebb462e86/yamlcore-0.1.1.tar.gz --output /work/sdist.tar.gz \
    && echo '7a3a7e83e659b7b282610b70a632ff27708b3315ac884890c0382476bf453f28  /work/sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sdist.tar.gz --strip-components=1 -C /work/sdist \
    && unzip -q /work/wheels/yamlcore-0.1.1-py3-none-any.whl -d /work/wheel \
    && diff -r /work/sdist/yamlcore /work/wheel/yamlcore \
    && grep -Fx 'License: MIT License' /work/wheel/yamlcore-0.1.1.dist-info/METADATA \
    && cd /work/sdist \
    && printf '%s\n' \
       'a12cea1e144d9de98710c2942020cb7b4d43c7337b86b924b6d074f63b74d9a1  yamlcore/__init__.py' \
       '251efad61eb34a539a6b85d09eab31d122f30059eaf87c31bf602b4fd4badaba  yamlcore/loader.py' \
       '6653e9802cad84163aaaca231ce7700826599f14505f04971f2e6df51ba24996  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/wheel/yamlcore /opt/venv/lib/python3.14/site-packages/yamlcore \
    && /opt/venv/bin/python -c 'import yaml, yamlcore; assert yaml.__version__ == "6.0.3"; assert issubclass(yamlcore.CoreLoader, yaml.BaseLoader); print(yaml.load(b"ready: true", Loader=yamlcore.CoreLoader))' \
    && { python3 --version; /opt/venv/bin/pip show yamlcore PyYAML atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum yamlcore/loader.py yamlcore/__init__.py yaml/scanner.py yaml/parser.py yaml/composer.py yaml/resolver.py; } > /work/toolchain.txt

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
