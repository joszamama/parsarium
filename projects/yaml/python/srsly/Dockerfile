FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# srsly 3.0.1: the wheel's Python package must match the pinned sdist byte for byte.
# ruamel.yaml 0.19.1 is the YAML parser srsly.yaml_loads calls; msgpack, ujson and
# cloudpickle are srsly's import-time dependencies for its other formats.
RUN mkdir /work/wheels /work/sdist /work/wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c6/fc/247e61b3e3962fa3b2eb79bd7f8eab08203c6f96cd3d4c205f95145c5f19/srsly-3.0.1-py2.py3-none-any.whl --output /work/wheels/srsly-3.0.1-py2.py3-none-any.whl \
    && echo '3f8f38da61fbec84cf2132d6ea90c8a358d00eaac9011244bceccd02abc69392  /work/wheels/srsly-3.0.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b8/0c/51f6841f1d84f404f92463fc2b1ba0da357ca1e3db6b7fbda26956c3b82a/ruamel_yaml-0.19.1-py3-none-any.whl --output /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl \
    && echo '27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93  /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/39/8f/bf975b5d2111e4954a0f8567fc6b60bab22c8766dd4fa509af1334c91a4f/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo '5d65b791ce4283e02b6267742ad540899155e1b32887b9cbdda47f38f5a076b5  /work/wheels/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/64/2b/3e322bf82d926d9857206cd5820438d78392d1f523dacecb8bd899952f73/ujson-5.12.0-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/ujson-5.12.0-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl \
    && echo '0e00cec383eab2406c9e006bd4edb55d284e94bb943fda558326048178d26961  /work/wheels/ujson-5.12.0-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/39/799be3f2f0f38cc727ee3b4f1445fe6d5e4133064ec2e4115069418a5bb6/cloudpickle-3.1.2-py3-none-any.whl --output /work/wheels/cloudpickle-3.1.2-py3-none-any.whl \
    && echo '9acb47f6afd73f60dc1df93bb801b472f05ff42fa6c84167d25cb206be1fbf4a  /work/wheels/cloudpickle-3.1.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/df/f5/a66bb23771c32d1bdccdb53ebff081268ef5896c5576b88ee6273e3d0558/srsly-3.0.1.tar.gz --output /work/sdist.tar.gz \
    && echo 'fd56c1876df09eebd0456175a72d7dd9a40f7fad545f777bcb2c40df8c4b0de9  /work/sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sdist.tar.gz --strip-components=1 -C /work/sdist \
    && unzip -q /work/wheels/srsly-3.0.1-py2.py3-none-any.whl -d /work/wheel \
    && diff -r /work/sdist/srsly /work/wheel/srsly \
    && grep -Fx 'License: MIT' /work/wheel/srsly-3.0.1.dist-info/METADATA \
    && cd /work/sdist \
    && printf '%s\n' \
       '04d78ede0623f3100bfcd4dea8d6a016ea1acbfbf66ffb511b2571c7627a3cfe  srsly/_yaml_api.py' \
       '03ad02b24d38c631ebb95816e1e50dc4cc1f15d13af1aea16ae4d09314619f15  srsly/__init__.py' \
       '6c9e9291cb685579e05a3f76c776cc5dee1ebd89d6823b93d5f875b96e4e5f11  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/wheel/srsly /opt/venv/lib/python3.14/site-packages/srsly \
    && /opt/venv/bin/python -c 'import srsly, srsly._yaml_api, ruamel.yaml, ruamel.yaml.parser; assert srsly.__version__ == "3.0.1" and ruamel.yaml.__version__ == "0.19.1"; assert srsly._yaml_api.CustomYaml().Parser is ruamel.yaml.parser.Parser; print(srsly.yaml_loads("ready: true"))' \
    && { python3 --version; /opt/venv/bin/pip show srsly ruamel.yaml msgpack ujson cloudpickle atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum srsly/_yaml_api.py ruamel/yaml/scanner.py ruamel/yaml/parser.py ruamel/yaml/composer.py ruamel/yaml/main.py; } > /work/toolchain.txt

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
