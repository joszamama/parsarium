FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# ruamel.yaml 0.19.1: the wheel's Python package must match the pinned sdist byte for byte.
RUN mkdir /work/wheels /work/sdist /work/wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b8/0c/51f6841f1d84f404f92463fc2b1ba0da357ca1e3db6b7fbda26956c3b82a/ruamel_yaml-0.19.1-py3-none-any.whl --output /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl \
    && echo '27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93  /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c7/3b/ebda527b56beb90cb7652cb1c7e4f91f48649fbcd8d2eb2fb6e77cd3329b/ruamel_yaml-0.19.1.tar.gz --output /work/sdist.tar.gz \
    && echo '53eb66cd27849eff968ebf8f0bf61f46cdac2da1d1f3576dd4ccee9b25c31993  /work/sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sdist.tar.gz --strip-components=1 -C /work/sdist \
    && unzip -q /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl -d /work/wheel \
    && diff -r --exclude=CHANGES --exclude=LICENSE --exclude=MANIFEST.in --exclude=PKG-INFO --exclude=README.md --exclude=pyproject.toml --exclude=setup.cfg --exclude=ruamel.yaml.egg-info --exclude=setup.py /work/sdist /work/wheel/ruamel/yaml \
    && grep -Fx 'License: MIT' /work/wheel/ruamel_yaml-0.19.1.dist-info/METADATA \
    && cd /work/sdist \
    && printf '%s\n' \
       'b716df08841b725be09153e1a093a1359a16044a395bc892a975f9b1509cc8ce  scanner.py' \
       '44b2d0b372807d08fa2175841ed3d1c974320a5858d238a1b8ba50cd77d78f9a  parser.py' \
       '981b0fd0db996cc109ac8639e66129a0e0a2b0b1ea615bc30ece99f4b9569778  composer.py' \
       'bdaace288852001493bff213299314bb5ff1d9d6aeca217c0c4f91fa61145298  constructor.py' \
       'aad8c7f2a4ffbff69a9aac646bc87440e7f6227f2cc6b2a914eeaa3b10d50171  resolver.py' \
       '5daf425f708a3a69f6877cd388a41b7d560670a7010f127c3dc7a055ebcf0b6c  reader.py' \
       'fa7fbcadac0b9f979fb14a653109bb831f95b94a4450caa896c14d2a10b571d6  main.py' \
       '43aba634d5da461169bb47f7180306323d0bb64f2d9c4e53e67d0b482dbc97d5  __init__.py' \
       '3e7632bb0dc1150f15f8161f5eec48dec8a99aaa1dfc9e8f63c02931e0fba7f8  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/wheel/ruamel/yaml /opt/venv/lib/python3.14/site-packages/ruamel/yaml \
    && /opt/venv/bin/python -c 'from ruamel.yaml import YAML, __version__; assert __version__ == "0.19.1"; y = YAML(typ="safe", pure=True); print(y.load(b"ready: true"))' \
    && { python3 --version; /opt/venv/bin/pip show ruamel.yaml atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum ruamel/yaml/scanner.py ruamel/yaml/parser.py ruamel/yaml/composer.py ruamel/yaml/constructor.py ruamel/yaml/resolver.py ruamel/yaml/reader.py ruamel/yaml/main.py; } > /work/toolchain.txt

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
